#!/usr/bin/env python3
"""
Add Audio Files to Xcode Project
Adds all voice MP3 files to the BennieGame Xcode project.
"""

import os
import re
import uuid
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent.parent
PROJECT_FILE = BASE_DIR / "BennieGame" / "BennieGame.xcodeproj" / "project.pbxproj"
AUDIO_BASE = BASE_DIR / "BennieGame" / "BennieGame" / "Resources" / "Audio" / "Voice"

def generate_uuid():
    """Generate Xcode-style UUID (24 hex chars)."""
    return uuid.uuid4().hex[:24].upper()

def find_audio_files():
    """Find all MP3 files in the Voice directory."""
    files = []
    for mp3_file in AUDIO_BASE.rglob("*.mp3"):
        relative = mp3_file.relative_to(AUDIO_BASE)
        files.append({
            "path": str(mp3_file),
            "relative": str(relative),
            "name": mp3_file.name,
            "folder": mp3_file.parent.name  # Narrator, Bennie, Success
        })
    return files

def main():
    print("=" * 60)
    print("Adding Audio Files to Xcode Project")
    print("=" * 60)

    # Find all audio files
    audio_files = find_audio_files()
    print(f"Found {len(audio_files)} audio files")

    # Read project file
    with open(PROJECT_FILE, "r") as f:
        content = f.read()

    # Find the Audio group UUID
    audio_group_match = re.search(r'([A-F0-9]{24}) /\* Audio \*/ = \{', content)
    if not audio_group_match:
        print("ERROR: Could not find Audio group in project file")
        return

    audio_group_uuid = audio_group_match.group(1)
    print(f"Audio group UUID: {audio_group_uuid}")

    # Find the Resources group in Copy Bundle Resources
    copy_resources_match = re.search(r'([A-F0-9]{24}) /\* Copy Bundle Resources \*/ = \{[^}]+files = \(([^)]*)\)', content, re.DOTALL)
    if not copy_resources_match:
        print("ERROR: Could not find Copy Bundle Resources section")
        return

    copy_resources_uuid = copy_resources_match.group(1)
    existing_resources = copy_resources_match.group(2)
    print(f"Copy Bundle Resources UUID: {copy_resources_uuid}")

    # Create entries for each file
    file_refs = []
    build_files = []
    group_children = {"Narrator": [], "Bennie": [], "Success": []}

    for audio_file in audio_files:
        file_uuid = generate_uuid()
        build_uuid = generate_uuid()
        name = audio_file["name"]
        folder = audio_file["folder"]
        relative_path = f"Voice/{audio_file['relative']}"

        # File reference entry
        file_refs.append(f'\t\t{file_uuid} /* {name} */ = {{isa = PBXFileReference; lastKnownFileType = audio.mp3; path = "{name}"; sourceTree = "<group>"; }};')

        # Build file entry
        build_files.append(f'\t\t{build_uuid} /* {name} in Copy Bundle Resources */ = {{isa = PBXBuildFile; fileRef = {file_uuid} /* {name} */; }};')

        # Group child
        group_children[folder].append(f'{file_uuid} /* {name} */')

    print(f"\nGenerated {len(file_refs)} file references")
    print(f"Generated {len(build_files)} build file entries")

    # Create Voice folder groups
    voice_uuid = generate_uuid()
    narrator_uuid = generate_uuid()
    bennie_uuid = generate_uuid()
    success_uuid = generate_uuid()

    # Create group entries
    narrator_children = ",\n\t\t\t\t".join(group_children["Narrator"])
    bennie_children = ",\n\t\t\t\t".join(group_children["Bennie"])
    success_children = ",\n\t\t\t\t".join(group_children["Success"])

    voice_group = f'''		{voice_uuid} /* Voice */ = {{
			isa = PBXGroup;
			children = (
				{narrator_uuid} /* Narrator */,
				{bennie_uuid} /* Bennie */,
				{success_uuid} /* Success */,
			);
			path = Voice;
			sourceTree = "<group>";
		}};'''

    narrator_group = f'''		{narrator_uuid} /* Narrator */ = {{
			isa = PBXGroup;
			children = (
				{narrator_children}
			);
			path = Narrator;
			sourceTree = "<group>";
		}};'''

    bennie_group = f'''		{bennie_uuid} /* Bennie */ = {{
			isa = PBXGroup;
			children = (
				{bennie_children}
			);
			path = Bennie;
			sourceTree = "<group>";
		}};'''

    success_group = f'''		{success_uuid} /* Success */ = {{
			isa = PBXGroup;
			children = (
				{success_children}
			);
			path = Success;
			sourceTree = "<group>";
		}};'''

    # Insert file references after existing PBXFileReference section marker
    file_ref_section_end = content.find("/* End PBXFileReference section */")
    if file_ref_section_end != -1:
        file_refs_str = "\n".join(file_refs) + "\n"
        content = content[:file_ref_section_end] + file_refs_str + content[file_ref_section_end:]
        print("Inserted file references")

    # Insert build files after existing PBXBuildFile section marker
    build_file_section_end = content.find("/* End PBXBuildFile section */")
    if build_file_section_end != -1:
        build_files_str = "\n".join(build_files) + "\n"
        content = content[:build_file_section_end] + build_files_str + content[build_file_section_end:]
        print("Inserted build files")

    # Insert groups after existing PBXGroup section marker
    group_section_end = content.find("/* End PBXGroup section */")
    if group_section_end != -1:
        groups_str = f"{voice_group}\n{narrator_group}\n{bennie_group}\n{success_group}\n"
        content = content[:group_section_end] + groups_str + content[group_section_end:]
        print("Inserted groups")

    # Update Audio group to include Voice folder
    audio_group_pattern = rf'({audio_group_uuid} /\* Audio \*/ = \{{\s*isa = PBXGroup;\s*children = \()([^)]*\))'
    audio_group_match = re.search(audio_group_pattern, content, re.DOTALL)
    if audio_group_match:
        old_children = audio_group_match.group(2)
        new_children = f"\n\t\t\t\t{voice_uuid} /* Voice */,\n\t\t\t" + old_children.lstrip()
        content = content.replace(audio_group_match.group(0),
                                  audio_group_match.group(1) + new_children)
        print("Updated Audio group children")

    # Add files to Copy Bundle Resources
    build_file_refs = [f.split("/*")[0].strip() for f in build_files]
    new_resources = existing_resources.rstrip()
    for ref in build_file_refs:
        name = [f["name"] for f in audio_files if ref.replace("\t\t", "") in content and f["name"] in content]
        if name:
            new_resources += f"\n\t\t\t\t{ref.strip()} /* {name[0]} in Copy Bundle Resources */,"

    content = content.replace(
        f"files = ({existing_resources})",
        f"files = ({new_resources}\n\t\t\t)"
    )
    print("Updated Copy Bundle Resources")

    # Write updated project file
    with open(PROJECT_FILE, "w") as f:
        f.write(content)

    print("\n" + "=" * 60)
    print("Project file updated!")
    print("=" * 60)
    print("\nPlease verify by opening Xcode and checking:")
    print("1. Resources/Audio/Voice folder shows in navigator")
    print("2. Build project to verify files are bundled")

if __name__ == "__main__":
    main()
