#!/usr/bin/env python3
import random

def randomize_photo_blocks():
    # Read the photos.txt file
    try:
        with open('photos.txt', 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("❌ photos.txt file not found!")
        return
    
    if not lines:
        print("❌ photos.txt is empty!")
        return
    
    # Parse the file into blocks
    # Each block is 4 lines followed by an empty line
    blocks = []
    current_block = []
    
    for line in lines:
        if line.strip() == '':  # Empty line
            if current_block:
                # We've finished a block, add it to blocks
                blocks.append(current_block)
                current_block = []
        else:
            # Add line to current block
            current_block.append(line)
    
    # Add any remaining block (in case file doesn't end with empty line)
    if current_block:
        blocks.append(current_block)
    
    if not blocks:
        print("❌ No photo blocks found in photos.txt!")
        return
    
    print(f"📸 Found {len(blocks)} photo blocks to randomize...")
    
    # Validate that blocks are 4 lines each (optional warning)
    for i, block in enumerate(blocks):
        if len(block) != 4:
            print(f"⚠️  Warning: Block {i+1} has {len(block)} lines instead of 4")
    
    # Randomize the blocks
    random.shuffle(blocks)
    
    # Reconstruct the file content
    new_content = []
    for i, block in enumerate(blocks):
        # Add the 4 lines of the block
        new_content.extend(block)
        # Add empty line after each block (except possibly the last one)
        if i < len(blocks) - 1:
            new_content.append('\n')
    
    # Write back to photos.txt
    with open('photos.txt', 'w', encoding='utf-8') as f:
        f.writelines(new_content)
    
    print("✅ Photo blocks have been randomized successfully!")
    print(f"🔄 Randomized {len(blocks)} blocks in photos.txt")

if __name__ == "__main__":
    randomize_photo_blocks()
