#!/usr/bin/env ruby
# Add Audio Files to Xcode Project using xcodeproj gem
require 'xcodeproj'
require 'pathname'

PROJECT_PATH = File.expand_path('../../BennieGame/BennieGame.xcodeproj', __FILE__)
AUDIO_PATH = File.expand_path('../../BennieGame/BennieGame/Resources/Audio/Voice', __FILE__)

puts "=" * 60
puts "Adding Audio Files to Xcode Project"
puts "=" * 60
puts "Project: #{PROJECT_PATH}"
puts "Audio: #{AUDIO_PATH}"

# Open project
project = Xcodeproj::Project.open(PROJECT_PATH)
target = project.targets.first

puts "\nTarget: #{target.name}"

# Find Resources group
resources_group = project.main_group.find_subpath('BennieGame/Resources', false)
unless resources_group
  puts "ERROR: Could not find Resources group"
  exit 1
end

# Find or create Audio group
audio_group = resources_group.find_subpath('Audio', false)
unless audio_group
  audio_group = resources_group.new_group('Audio', 'Audio')
end

# Find or create Voice group
voice_group = audio_group.find_subpath('Voice', false)
if voice_group
  puts "Removing existing Voice group..."
  voice_group.remove_from_project
end

# Add Voice folder as a group with all files
voice_group = audio_group.new_group('Voice', 'Voice')

# Add each subfolder
['Narrator', 'Bennie', 'Success'].each do |folder|
  folder_path = File.join(AUDIO_PATH, folder)
  next unless File.directory?(folder_path)

  sub_group = voice_group.new_group(folder, folder)

  Dir.glob(File.join(folder_path, '*.mp3')).sort.each do |file|
    filename = File.basename(file)

    # Check if file already exists in group
    existing = sub_group.files.find { |f| f.path == filename }
    if existing
      puts "  Skipping (exists): #{folder}/#{filename}"
      next
    end

    # Add file reference
    file_ref = sub_group.new_file(filename)

    # Add to Copy Bundle Resources build phase
    target.resources_build_phase.add_file_reference(file_ref)

    puts "  Added: #{folder}/#{filename}"
  end
end

# Save project
project.save
puts "\n" + "=" * 60
puts "Project saved successfully!"
puts "=" * 60
puts "\nVerify by rebuilding the project"
