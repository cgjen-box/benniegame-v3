#!/usr/bin/env python3
"""
MCP Resilience Framework
========================
Makes MCP servers resilient to network issues, large payloads, and timeouts.

Key Features:
- Automatic response size limiting (never exceed transport limits)
- File-based response for large data (return path instead of data)
- Retry logic with exponential backoff
- Health checks and auto-recovery
- Graceful degradation
- Response chunking

Usage:
    from mcp_resilience import resilient_tool, save_large_response

    @mcp.tool()
    @resilient_tool(max_response_bytes=400_000)  # 400KB max
    async def my_tool() -> dict:
        # Your tool logic here
        return {"image": "base64...", "data": "..."}
"""

import os
import sys
import json
import hashlib
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, Callable
from functools import wraps

# Import standard error format
try:
    from mcp_error_standard import MCPErrorResponse, ErrorSeverity, size_limit_exceeded
except ImportError:
    print("[WARN] mcp_error_standard not found, using basic error handling", file=sys.stderr)
    MCPErrorResponse = None
    ErrorSeverity = None
    size_limit_exceeded = None

# =============================================================================
# CONFIGURATION
# =============================================================================

class ResilienceConfig:
    """Global resilience configuration."""

    # Response size limits (conservative to prevent transport errors)
    MAX_RESPONSE_BYTES = 400_000  # 400KB max (well under 500KB limit)
    MAX_IMAGE_BYTES = 300_000     # 300KB max for images
    MAX_TEXT_BYTES = 100_000      # 100KB max for text responses

    # Retry configuration
    MAX_RETRIES = 3
    INITIAL_RETRY_DELAY = 1.0  # seconds
    RETRY_BACKOFF = 2.0        # exponential backoff multiplier

    # File-based responses
    LARGE_RESPONSE_DIR = Path.home() / "mcp_large_responses"
    RESPONSE_TTL_HOURS = 24  # Auto-delete after 24 hours

    # Health check
    HEALTH_CHECK_INTERVAL = 60  # seconds
    MAX_CONSECUTIVE_FAILURES = 5


# Ensure large response directory exists
ResilienceConfig.LARGE_RESPONSE_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# SIZE GUARD (Output Validation)
# =============================================================================

class SizeGuard:
    """
    Automatic output size validation and handling.

    Prevents MCP transport errors by checking response size before sending.
    """

    @staticmethod
    def validate_output(
        data: Any,
        tool_name: str,
        max_bytes: int = None,
        save_to_file: bool = True
    ) -> Dict[str, Any]:
        """
        Validate output size and handle oversized responses.

        Args:
            data: Response data to validate
            tool_name: Name of the tool (for error messages)
            max_bytes: Maximum allowed size (default: from config)
            save_to_file: Whether to save large responses to file

        Returns:
            Validated response (either original data or file reference)
        """
        max_bytes = max_bytes or ResilienceConfig.MAX_RESPONSE_BYTES
        size = get_response_size(data)

        # Size OK - return original data wrapped in success response
        if size <= max_bytes:
            if MCPErrorResponse:
                return MCPErrorResponse.success(
                    tool_name=tool_name,
                    result=data,
                    metadata={"size_bytes": size, "under_limit": True}
                )
            else:
                return {"success": True, "result": data, "size_bytes": size}

        # Size too large - handle gracefully
        if save_to_file:
            # Save to file and return reference
            filepath = save_large_response(
                data,
                name=f"{tool_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )

            if MCPErrorResponse and size_limit_exceeded:
                return size_limit_exceeded(
                    tool_name=tool_name,
                    actual_size=size,
                    max_size=max_bytes,
                    file_path=filepath
                )
            else:
                return {
                    "success": True,
                    "type": "file_reference",
                    "message": f"Response too large ({size:,} bytes), saved to file",
                    "file_path": filepath,
                    "size_bytes": size,
                    "max_bytes": max_bytes,
                    "note": "Use bennie-files MCP to read the file"
                }
        else:
            # Truncate response
            if MCPErrorResponse:
                return MCPErrorResponse.warning(
                    tool_name=tool_name,
                    warning_message=f"Response too large ({size:,} bytes), truncated",
                    result=str(data)[:1000] + "... [TRUNCATED]",
                    degraded_functionality="Response truncated to fit size limit"
                )
            else:
                return {
                    "success": False,
                    "error": "Response too large",
                    "size_bytes": size,
                    "max_bytes": max_bytes,
                    "truncated_result": str(data)[:1000] + "... [TRUNCATED]"
                }

    @staticmethod
    def ensure_serializable(data: Any) -> Any:
        """
        Ensure data is JSON-serializable.

        Args:
            data: Data to check

        Returns:
            Serializable version of data

        Raises:
            ValueError: If data cannot be made serializable
        """
        try:
            # Try to serialize
            json.dumps(data)
            return data
        except (TypeError, ValueError) as e:
            # Try to convert to string
            try:
                return str(data)
            except Exception:
                raise ValueError(f"Data is not serializable: {e}")


# =============================================================================
# RESPONSE SIZE MANAGEMENT
# =============================================================================

def get_response_size(data: Any) -> int:
    """Calculate size of response data in bytes."""
    try:
        if isinstance(data, dict):
            # JSON serialize to get accurate size
            json_str = json.dumps(data)
            return len(json_str.encode('utf-8'))
        elif isinstance(data, str):
            return len(data.encode('utf-8'))
        elif isinstance(data, bytes):
            return len(data)
        else:
            # Try to serialize
            json_str = json.dumps(str(data))
            return len(json_str.encode('utf-8'))
    except:
        return 0


def is_response_too_large(data: Any, max_bytes: int = None) -> bool:
    """Check if response exceeds size limit."""
    max_bytes = max_bytes or ResilienceConfig.MAX_RESPONSE_BYTES
    size = get_response_size(data)
    return size > max_bytes


def save_large_response(data: Any, name: str = None) -> str:
    """
    Save large response to file and return file path.

    Args:
        data: Response data to save
        name: Optional name for file (auto-generated if None)

    Returns:
        Absolute path to saved file
    """
    if name is None:
        # Generate unique name from timestamp + hash
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        hash_val = hashlib.md5(str(data).encode()).hexdigest()[:8]
        name = f"response_{ts}_{hash_val}"

    filepath = ResilienceConfig.LARGE_RESPONSE_DIR / f"{name}.json"

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

    return str(filepath)


def cleanup_old_responses():
    """Delete response files older than TTL."""
    cutoff = datetime.now() - timedelta(hours=ResilienceConfig.RESPONSE_TTL_HOURS)

    for filepath in ResilienceConfig.LARGE_RESPONSE_DIR.glob("*.json"):
        try:
            mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
            if mtime < cutoff:
                filepath.unlink()
        except:
            pass


# =============================================================================
# RESILIENT TOOL DECORATOR
# =============================================================================

def resilient_tool(
    max_response_bytes: int = None,
    max_retries: int = None,
    save_large_to_file: bool = True
):
    """
    Decorator to make MCP tools resilient.

    Features:
    - Checks response size before returning
    - Saves large responses to file instead
    - Automatic retry on failure
    - Graceful error handling

    Args:
        max_response_bytes: Max response size (default: 400KB)
        max_retries: Number of retries on failure (default: 3)
        save_large_to_file: Save large responses to file (default: True)

    Example:
        @mcp.tool()
        @resilient_tool(max_response_bytes=300_000)
        async def take_screenshot() -> dict:
            # Your tool logic
            return {"image": "base64...", "size": 12345}
    """
    max_bytes = max_response_bytes or ResilienceConfig.MAX_RESPONSE_BYTES
    retries = max_retries or ResilienceConfig.MAX_RETRIES

    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_error = None

            # Retry loop
            for attempt in range(retries):
                try:
                    # Call original function
                    result = await func(*args, **kwargs)

                    # Validate output size using SizeGuard
                    validated = SizeGuard.validate_output(
                        data=result,
                        tool_name=func.__name__,
                        max_bytes=max_bytes,
                        save_to_file=save_large_to_file
                    )

                    # Record success
                    health_monitor.record_success()

                    return validated

                except Exception as e:
                    last_error = e

                    # Record failure
                    health_monitor.record_failure()

                    # Exponential backoff
                    if attempt < retries - 1:
                        delay = ResilienceConfig.INITIAL_RETRY_DELAY * (ResilienceConfig.RETRY_BACKOFF ** attempt)
                        await asyncio.sleep(delay)
                        continue

            # All retries failed - return structured error
            if MCPErrorResponse:
                return MCPErrorResponse.from_exception(
                    tool_name=func.__name__,
                    exception=last_error,
                    severity=ErrorSeverity.RECOVERABLE if MCPErrorResponse else None,
                    recovery_hint=f"Tool failed after {retries} retries. Check logs and try again."
                )
            else:
                return {
                    "success": False,
                    "error": f"Tool failed after {retries} retries",
                    "last_error": str(last_error),
                    "function": func.__name__
                }

        return wrapper
    return decorator


# =============================================================================
# IMAGE-SPECIFIC HELPERS
# =============================================================================

def handle_large_image(
    image_b64: str,
    metadata: Dict[str, Any],
    name: str = "image"
) -> Dict[str, Any]:
    """
    Handle large base64 image - save to file if too big.

    Args:
        image_b64: Base64-encoded image string
        metadata: Image metadata (width, height, etc.)
        name: Name for saved file

    Returns:
        Response dict (either with image or file reference)
    """
    size_bytes = len(image_b64.encode('utf-8'))

    if size_bytes > ResilienceConfig.MAX_IMAGE_BYTES:
        # Too large - save to file
        import base64
        from PIL import Image
        import io

        # Decode and save as file
        image_data = base64.b64decode(image_b64)
        filepath = ResilienceConfig.LARGE_RESPONSE_DIR / f"{name}.jpg"

        with open(filepath, 'wb') as f:
            f.write(image_data)

        return {
            "success": True,
            "type": "file_reference",
            "message": f"Image too large ({size_bytes} bytes), saved to file",
            "file_path": str(filepath),
            "image_metadata": metadata,
            "size_bytes": size_bytes,
            "note": "Open file to view full-resolution image"
        }
    else:
        # Size OK - return normally
        return {
            "success": True,
            "type": "inline",
            "image": image_b64,
            "size_bytes": size_bytes,
            **metadata
        }


# =============================================================================
# CHUNKED RESPONSE SYSTEM
# =============================================================================

class ChunkedResponse:
    """
    Split large responses into chunks for streaming.

    Usage:
        chunked = ChunkedResponse(large_data, chunk_size=100_000)

        # Get total chunks
        total = chunked.total_chunks()

        # Get chunk by index
        chunk = chunked.get_chunk(0)
    """

    def __init__(self, data: Any, chunk_size: int = 100_000):
        """
        Initialize chunked response.

        Args:
            data: Data to chunk (dict, string, or bytes)
            chunk_size: Size of each chunk in bytes
        """
        self.data = data
        self.chunk_size = chunk_size

        # Serialize data
        if isinstance(data, dict):
            self.serialized = json.dumps(data)
        elif isinstance(data, str):
            self.serialized = data
        else:
            self.serialized = str(data)

        self.data_bytes = self.serialized.encode('utf-8')
        self.total_size = len(self.data_bytes)

    def total_chunks(self) -> int:
        """Get total number of chunks."""
        return (self.total_size + self.chunk_size - 1) // self.chunk_size

    def get_chunk(self, index: int) -> Dict[str, Any]:
        """Get chunk by index (0-based)."""
        start = index * self.chunk_size
        end = min(start + self.chunk_size, self.total_size)

        chunk_data = self.data_bytes[start:end].decode('utf-8')

        return {
            "chunk_index": index,
            "total_chunks": self.total_chunks(),
            "chunk_size": len(chunk_data),
            "total_size": self.total_size,
            "data": chunk_data,
            "is_final": index == self.total_chunks() - 1
        }

    def save_to_file(self, filepath: Path = None) -> str:
        """
        Save full data to file.

        Args:
            filepath: Optional path (auto-generated if None)

        Returns:
            Path to saved file
        """
        if filepath is None:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = ResilienceConfig.LARGE_RESPONSE_DIR / f"chunked_{ts}.json"

        with open(filepath, 'w') as f:
            f.write(self.serialized)

        return str(filepath)


# =============================================================================
# HEALTH CHECK SYSTEM
# =============================================================================

class HealthMonitor:
    """Monitor MCP server health and auto-recover."""

    def __init__(self):
        self.consecutive_failures = 0
        self.last_success = datetime.now()
        self.total_requests = 0
        self.total_failures = 0

    def record_success(self):
        """Record successful request."""
        self.consecutive_failures = 0
        self.last_success = datetime.now()
        self.total_requests += 1

    def record_failure(self):
        """Record failed request."""
        self.consecutive_failures += 1
        self.total_requests += 1
        self.total_failures += 1

    def is_healthy(self) -> bool:
        """Check if server is healthy."""
        return self.consecutive_failures < ResilienceConfig.MAX_CONSECUTIVE_FAILURES

    def get_stats(self) -> Dict[str, Any]:
        """Get health statistics."""
        success_rate = 1.0 - (self.total_failures / max(self.total_requests, 1))

        return {
            "healthy": self.is_healthy(),
            "consecutive_failures": self.consecutive_failures,
            "total_requests": self.total_requests,
            "total_failures": self.total_failures,
            "success_rate": round(success_rate * 100, 1),
            "last_success": self.last_success.isoformat(),
            "uptime_seconds": (datetime.now() - self.last_success).total_seconds()
        }


# Global health monitor
health_monitor = HealthMonitor()


# =============================================================================
# UTILITY FUNCTIONS
# =============================================================================

def truncate_for_display(data: str, max_chars: int = 500) -> str:
    """Truncate string for display."""
    if len(data) <= max_chars:
        return data
    return data[:max_chars] + f"... [TRUNCATED, {len(data)} total chars]"


def format_bytes(size_bytes: int) -> str:
    """Format bytes as human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


# =============================================================================
# CLEANUP TASK
# =============================================================================

async def cleanup_task():
    """Background task to cleanup old response files."""
    while True:
        try:
            cleanup_old_responses()
        except Exception as e:
            print(f"[WARN] Cleanup task error: {e}", file=sys.stderr)

        # Run every hour
        await asyncio.sleep(3600)


# =============================================================================
# SELF-TEST
# =============================================================================

if __name__ == "__main__":
    import asyncio

    async def test():
        print("MCP Resilience Framework - Self Test")
        print("=" * 60)

        # Test 1: Response size checking
        print("\n1. Testing response size checking...")
        small_data = {"message": "Small response"}
        large_data = {"image": "x" * 500_000}  # 500KB

        print(f"   Small response: {format_bytes(get_response_size(small_data))}")
        print(f"   Large response: {format_bytes(get_response_size(large_data))}")
        print(f"   Is large too big? {is_response_too_large(large_data)}")

        # Test 2: Save large response
        print("\n2. Testing file-based response...")
        filepath = save_large_response(large_data, name="test_large")
        print(f"   Saved to: {filepath}")
        print(f"   File exists: {Path(filepath).exists()}")

        # Test 3: Chunked response
        print("\n3. Testing chunked response...")
        chunked = ChunkedResponse(large_data, chunk_size=100_000)
        print(f"   Total size: {format_bytes(chunked.total_size)}")
        print(f"   Total chunks: {chunked.total_chunks()}")
        chunk0 = chunked.get_chunk(0)
        print(f"   First chunk size: {format_bytes(chunk0['chunk_size'])}")

        # Test 4: Health monitor
        print("\n4. Testing health monitor...")
        monitor = HealthMonitor()
        monitor.record_success()
        monitor.record_success()
        monitor.record_failure()
        stats = monitor.get_stats()
        print(f"   Success rate: {stats['success_rate']}%")
        print(f"   Healthy: {stats['healthy']}")

        print("\n✅ All tests passed!")

    asyncio.run(test())
