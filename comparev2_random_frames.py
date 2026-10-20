"""
Random Frame Selection Module for Enhanced Screenshot Comparison Tool

This module adds random frame selection capability to the screenshot comparison tool.
It intelligently selects 30-35 random frames distributed throughout the video.
"""

import random
from typing import List, Tuple


def select_random_frames(
    total_frames: int,
    num_frames: int = 33,
    avoid_start_frames: int = 100,
    avoid_end_frames: int = 100,
    min_distance: int = 50
) -> List[int]:
    """
    Select random frames from a video with intelligent distribution.

    Args:
        total_frames: Total number of frames in the video
        num_frames: Number of frames to select (default 33, range 30-35)
        avoid_start_frames: Frames to skip at the beginning (avoid openings/logos)
        avoid_end_frames: Frames to skip at the end (avoid credits)
        min_distance: Minimum distance between selected frames

    Returns:
        List of frame numbers sorted in ascending order
    """
    # Validate inputs
    if total_frames < 1000:
        raise ValueError("Video too short for random frame selection (minimum 1000 frames)")

    # Randomize the number of frames slightly (30-35)
    if num_frames == 33:  # Only randomize if using default
        num_frames = random.randint(30, 35)

    # Calculate usable frame range
    start_frame = avoid_start_frames
    end_frame = total_frames - avoid_end_frames
    usable_frames = end_frame - start_frame

    if usable_frames < num_frames * min_distance:
        # If video is too short for min_distance, reduce it
        min_distance = usable_frames // (num_frames + 1)
        if min_distance < 1:
            min_distance = 1

    # Method 1: Divide video into segments and pick one random frame from each segment
    # This ensures good distribution across the entire video
    selected_frames = []
    segment_size = usable_frames / num_frames

    for i in range(num_frames):
        segment_start = int(start_frame + (i * segment_size))
        segment_end = int(start_frame + ((i + 1) * segment_size))

        # Pick a random frame within this segment
        if segment_start < segment_end:
            frame = random.randint(segment_start, segment_end - 1)
            selected_frames.append(frame)
        else:
            selected_frames.append(segment_start)

    # Method 2: Apply jitter to avoid too regular spacing
    # Adjust frames slightly while respecting min_distance
    jittered_frames = []
    for i, frame in enumerate(selected_frames):
        # Calculate safe jitter range
        max_jitter = min_distance // 4  # 25% of min_distance

        if i == 0:
            # First frame: jitter forward only
            jitter = random.randint(0, max_jitter)
        elif i == len(selected_frames) - 1:
            # Last frame: jitter backward only
            jitter = random.randint(-max_jitter, 0)
        else:
            # Middle frames: jitter both ways
            jitter = random.randint(-max_jitter, max_jitter)

        jittered_frame = frame + jitter

        # Ensure we don't go out of bounds
        jittered_frame = max(start_frame, min(jittered_frame, end_frame - 1))

        jittered_frames.append(jittered_frame)

    # Sort frames and ensure uniqueness
    final_frames = sorted(list(set(jittered_frames)))

    # If we lost frames due to duplicates, fill in the gaps
    while len(final_frames) < num_frames:
        # Find the largest gap between frames
        largest_gap = 0
        gap_index = 0

        for i in range(len(final_frames) - 1):
            gap = final_frames[i + 1] - final_frames[i]
            if gap > largest_gap:
                largest_gap = gap
                gap_index = i

        # Insert a frame in the middle of the largest gap
        if largest_gap > 1:
            new_frame = (final_frames[gap_index] + final_frames[gap_index + 1]) // 2
            final_frames.insert(gap_index + 1, new_frame)
        else:
            # If all gaps are 1, just add a frame before the last one
            final_frames.insert(-1, final_frames[-1] - 1)

        final_frames = sorted(list(set(final_frames)))

    # Trim to exact number if we have too many
    final_frames = final_frames[:num_frames]

    return final_frames


def select_random_frames_uniform(
    total_frames: int,
    num_frames: int = 33,
    avoid_start_frames: int = 100,
    avoid_end_frames: int = 100
) -> List[int]:
    """
    Simple uniform random frame selection.

    This is a simpler alternative that just picks completely random frames
    from the usable range without trying to distribute them.

    Args:
        total_frames: Total number of frames in the video
        num_frames: Number of frames to select
        avoid_start_frames: Frames to skip at the beginning
        avoid_end_frames: Frames to skip at the end

    Returns:
        List of frame numbers sorted in ascending order
    """
    # Randomize the number of frames slightly (30-35)
    if num_frames == 33:
        num_frames = random.randint(30, 35)

    # Calculate usable range
    start_frame = avoid_start_frames
    end_frame = total_frames - avoid_end_frames

    # Pick random frames
    frames = random.sample(range(start_frame, end_frame), num_frames)

    return sorted(frames)


def get_frame_distribution_stats(frames: List[int], total_frames: int) -> dict:
    """
    Calculate statistics about frame distribution.

    Args:
        frames: List of selected frame numbers
        total_frames: Total frames in video

    Returns:
        Dictionary with statistics
    """
    if not frames or len(frames) < 2:
        return {}

    # Calculate gaps between consecutive frames
    gaps = [frames[i + 1] - frames[i] for i in range(len(frames) - 1)]

    return {
        'count': len(frames),
        'first_frame': frames[0],
        'last_frame': frames[-1],
        'coverage_start': frames[0],
        'coverage_end': frames[-1],
        'coverage_percent': ((frames[-1] - frames[0]) / total_frames) * 100,
        'min_gap': min(gaps),
        'max_gap': max(gaps),
        'avg_gap': sum(gaps) / len(gaps),
        'median_gap': sorted(gaps)[len(gaps) // 2],
    }


# Example usage and testing
if __name__ == "__main__":
    # Test with a typical anime episode (24 fps, 24 minutes)
    total_frames = 24 * 60 * 24  # 34,560 frames

    print("Testing Random Frame Selection")
    print("=" * 60)
    print(f"Total frames: {total_frames}")
    print()

    # Test distributed selection
    print("Method 1: Distributed Selection")
    frames = select_random_frames(total_frames)
    stats = get_frame_distribution_stats(frames, total_frames)

    print(f"Selected {len(frames)} frames")
    print(f"First frame: {frames[0]}")
    print(f"Last frame: {frames[-1]}")
    print(f"Coverage: {stats['coverage_percent']:.1f}% of video")
    print(f"Average gap: {stats['avg_gap']:.0f} frames ({stats['avg_gap'] / 24:.1f} seconds)")
    print(f"Frame numbers: {frames[:10]}... (showing first 10)")
    print()

    # Test uniform selection
    print("Method 2: Uniform Random Selection")
    frames2 = select_random_frames_uniform(total_frames)
    stats2 = get_frame_distribution_stats(frames2, total_frames)

    print(f"Selected {len(frames2)} frames")
    print(f"First frame: {frames2[0]}")
    print(f"Last frame: {frames2[-1]}")
    print(f"Coverage: {stats2['coverage_percent']:.1f}% of video")
    print(f"Average gap: {stats2['avg_gap']:.0f} frames ({stats2['avg_gap'] / 24:.1f} seconds)")
    print(f"Frame numbers: {frames2[:10]}... (showing first 10)")
