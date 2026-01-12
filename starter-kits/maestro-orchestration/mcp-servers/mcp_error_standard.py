#!/usr/bin/env python3
"""
MCP Standard Error Format
=========================
Provides consistent, actionable error responses for all MCP tools.

Ensures Claude Desktop receives structured errors instead of crashes.

Usage:
    from mcp_error_standard import MCPErrorResponse, ErrorSeverity

    # Return a recoverable error
    return MCPErrorResponse.recoverable(
        tool_name="take_screenshot",
        error_message="Screenshot failed, device disconnected",
        recovery_hint="Try rebooting the simulator with boot_simulator()"
    )

    # Return a fatal error (tool unavailable)
    return MCPErrorResponse.fatal(
        tool_name="build_and_deploy",
        error_message="Xcode not installed",
        recovery_hint="This tool is not available. Please continue with other tasks."
    )
"""

from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime


class ErrorSeverity(Enum):
    """Error severity levels for MCP tools."""
    INFO = "info"              # Informational, no action needed
    WARNING = "warning"        # Degraded functionality, can continue
    RECOVERABLE = "recoverable"  # Error occurred, retry may succeed
    FATAL = "fatal"            # Tool unavailable, cannot proceed


class MCPErrorResponse:
    """Standard error response format for all MCP tools."""

    @staticmethod
    def success(
        tool_name: str,
        result: Any,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Standard success response.

        Args:
            tool_name: Name of the tool that succeeded
            result: The actual result data
            metadata: Optional metadata (timing, size, etc.)

        Returns:
            Standardized success response
        """
        response = {
            "success": True,
            "tool": tool_name,
            "timestamp": datetime.now().isoformat(),
            "result": result
        }

        if metadata:
            response["metadata"] = metadata

        return response

    @staticmethod
    def info(
        tool_name: str,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Informational message (not an error).

        Args:
            tool_name: Name of the tool
            message: Informational message
            details: Optional additional details

        Returns:
            Standardized info response
        """
        response = {
            "success": True,
            "severity": ErrorSeverity.INFO.value,
            "tool": tool_name,
            "timestamp": datetime.now().isoformat(),
            "message": message
        }

        if details:
            response["details"] = details

        return response

    @staticmethod
    def warning(
        tool_name: str,
        warning_message: str,
        result: Any = None,
        degraded_functionality: str = None
    ) -> Dict[str, Any]:
        """
        Warning response (degraded but functional).

        Args:
            tool_name: Name of the tool
            warning_message: What went wrong
            result: Partial result if available
            degraded_functionality: What functionality is limited

        Returns:
            Standardized warning response
        """
        response = {
            "success": True,
            "severity": ErrorSeverity.WARNING.value,
            "tool": tool_name,
            "timestamp": datetime.now().isoformat(),
            "warning": warning_message
        }

        if result is not None:
            response["result"] = result

        if degraded_functionality:
            response["degraded_functionality"] = degraded_functionality

        response["note"] = "Tool completed with warnings. You can continue."

        return response

    @staticmethod
    def recoverable(
        tool_name: str,
        error_message: str,
        recovery_hint: str,
        retry_after_seconds: Optional[int] = None,
        error_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Recoverable error (retry may succeed).

        Args:
            tool_name: Name of the tool that failed
            error_message: What went wrong
            recovery_hint: How to recover (for Claude to understand)
            retry_after_seconds: Suggested retry delay
            error_code: Optional error code for tracking

        Returns:
            Standardized recoverable error response
        """
        response = {
            "success": False,
            "severity": ErrorSeverity.RECOVERABLE.value,
            "tool": tool_name,
            "timestamp": datetime.now().isoformat(),
            "error": error_message,
            "recovery_hint": recovery_hint,
            "actionable": True,
            "note": "This error may be temporary. Please try the recovery hint and continue."
        }

        if retry_after_seconds:
            response["retry_after_seconds"] = retry_after_seconds

        if error_code:
            response["error_code"] = error_code

        return response

    @staticmethod
    def fatal(
        tool_name: str,
        error_message: str,
        recovery_hint: str = "This tool is not available. Please continue with other tasks.",
        permanent: bool = True,
        error_code: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Fatal error (tool unavailable, cannot proceed).

        Args:
            tool_name: Name of the tool that failed
            error_message: What went wrong
            recovery_hint: Guidance for Claude (default: continue without this tool)
            permanent: Whether this is a permanent failure
            error_code: Optional error code for tracking

        Returns:
            Standardized fatal error response
        """
        response = {
            "success": False,
            "severity": ErrorSeverity.FATAL.value,
            "tool": tool_name,
            "timestamp": datetime.now().isoformat(),
            "error": error_message,
            "recovery_hint": recovery_hint,
            "actionable": False,
            "permanent": permanent,
            "note": "This tool is unavailable. Please continue with other available tools."
        }

        if error_code:
            response["error_code"] = error_code

        return response

    @staticmethod
    def from_exception(
        tool_name: str,
        exception: Exception,
        severity: ErrorSeverity = ErrorSeverity.RECOVERABLE,
        recovery_hint: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create error response from Python exception.

        Args:
            tool_name: Name of the tool that raised exception
            exception: The exception object
            severity: Error severity level
            recovery_hint: Optional recovery guidance

        Returns:
            Standardized error response
        """
        error_message = f"{type(exception).__name__}: {str(exception)}"

        if severity == ErrorSeverity.FATAL:
            return MCPErrorResponse.fatal(
                tool_name=tool_name,
                error_message=error_message,
                recovery_hint=recovery_hint or "This tool encountered a fatal error. Please continue with other tasks."
            )
        elif severity == ErrorSeverity.RECOVERABLE:
            return MCPErrorResponse.recoverable(
                tool_name=tool_name,
                error_message=error_message,
                recovery_hint=recovery_hint or "Try again or use alternative tools to continue."
            )
        elif severity == ErrorSeverity.WARNING:
            return MCPErrorResponse.warning(
                tool_name=tool_name,
                warning_message=error_message
            )
        else:
            return MCPErrorResponse.info(
                tool_name=tool_name,
                message=error_message
            )


# Convenience functions for common error scenarios

def size_limit_exceeded(
    tool_name: str,
    actual_size: int,
    max_size: int,
    file_path: Optional[str] = None
) -> Dict[str, Any]:
    """Response when output exceeds size limit."""
    response = MCPErrorResponse.warning(
        tool_name=tool_name,
        warning_message=f"Response size ({actual_size:,} bytes) exceeds limit ({max_size:,} bytes)",
        degraded_functionality="Large response saved to file instead of returning inline"
    )

    if file_path:
        response["file_path"] = file_path
        response["recovery_hint"] = f"Use bennie-files MCP to read: {file_path}"
    else:
        response["recovery_hint"] = "Response was truncated. Please continue with partial result."

    return response


def timeout_error(
    tool_name: str,
    timeout_seconds: int,
    operation: str
) -> Dict[str, Any]:
    """Response when operation times out."""
    return MCPErrorResponse.recoverable(
        tool_name=tool_name,
        error_message=f"Operation '{operation}' timed out after {timeout_seconds}s",
        recovery_hint="Try again with more time, or break the operation into smaller steps.",
        retry_after_seconds=5
    )


def dependency_missing(
    tool_name: str,
    dependency_name: str,
    install_hint: Optional[str] = None
) -> Dict[str, Any]:
    """Response when required dependency is missing."""
    recovery_hint = install_hint or f"Install {dependency_name} to enable this tool."

    return MCPErrorResponse.fatal(
        tool_name=tool_name,
        error_message=f"Required dependency not found: {dependency_name}",
        recovery_hint=f"{recovery_hint} Please continue with other available tools.",
        permanent=True
    )


def invalid_input(
    tool_name: str,
    parameter_name: str,
    actual_value: Any,
    expected: str
) -> Dict[str, Any]:
    """Response when input validation fails."""
    return MCPErrorResponse.recoverable(
        tool_name=tool_name,
        error_message=f"Invalid input for '{parameter_name}': got {actual_value}, expected {expected}",
        recovery_hint=f"Please provide a valid value for '{parameter_name}' ({expected}) and try again."
    )


# =============================================================================
# SELF-TEST
# =============================================================================

if __name__ == "__main__":
    print("MCP Standard Error Format - Self Test")
    print("=" * 60)

    # Test 1: Success response
    print("\n1. Success Response:")
    success = MCPErrorResponse.success(
        tool_name="take_screenshot",
        result={"image": "base64...", "size": 91000},
        metadata={"compression_ratio": 0.032}
    )
    print(f"   ✅ {success}")

    # Test 2: Info response
    print("\n2. Info Response:")
    info = MCPErrorResponse.info(
        tool_name="boot_simulator",
        message="Simulator already booted"
    )
    print(f"   ℹ️  {info}")

    # Test 3: Warning response
    print("\n3. Warning Response:")
    warning = MCPErrorResponse.warning(
        tool_name="build_and_deploy",
        warning_message="Build succeeded with warnings",
        degraded_functionality="Some optimizations disabled"
    )
    print(f"   ⚠️  {warning}")

    # Test 4: Recoverable error
    print("\n4. Recoverable Error:")
    recoverable = MCPErrorResponse.recoverable(
        tool_name="launch_app",
        error_message="App not installed on simulator",
        recovery_hint="Run build_and_deploy() first to install the app"
    )
    print(f"   🔄 {recoverable}")

    # Test 5: Fatal error
    print("\n5. Fatal Error:")
    fatal = MCPErrorResponse.fatal(
        tool_name="run_tests",
        error_message="Xcode not installed",
        recovery_hint="This tool is not available. Please continue with other tasks."
    )
    print(f"   ❌ {fatal}")

    # Test 6: Size limit exceeded
    print("\n6. Size Limit Exceeded:")
    size_error = size_limit_exceeded(
        tool_name="take_screenshot",
        actual_size=2_000_000,
        max_size=300_000,
        file_path="~/mcp_large_responses/screenshot.jpg"
    )
    print(f"   📦 {size_error}")

    # Test 7: Timeout
    print("\n7. Timeout Error:")
    timeout = timeout_error(
        tool_name="build_and_deploy",
        timeout_seconds=300,
        operation="xcodebuild"
    )
    print(f"   ⏱️  {timeout}")

    # Test 8: Missing dependency
    print("\n8. Missing Dependency:")
    missing_dep = dependency_missing(
        tool_name="take_screenshot",
        dependency_name="Pillow",
        install_hint="pip install Pillow"
    )
    print(f"   📦 {missing_dep}")

    # Test 9: Invalid input
    print("\n9. Invalid Input:")
    invalid = invalid_input(
        tool_name="tap",
        parameter_name="x",
        actual_value=-10,
        expected="positive integer (0-1194)"
    )
    print(f"   ⚠️  {invalid}")

    # Test 10: From exception
    print("\n10. From Exception:")
    try:
        raise ValueError("Invalid coordinate")
    except Exception as e:
        exc_error = MCPErrorResponse.from_exception(
            tool_name="tap",
            exception=e,
            severity=ErrorSeverity.RECOVERABLE,
            recovery_hint="Provide valid x,y coordinates and try again"
        )
        print(f"   🐛 {exc_error}")

    print("\n✅ All tests passed!")
