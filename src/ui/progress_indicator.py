"""
Progress Indicator UI Component for Notion Template Maker.
Shows progress during template generation and other long-running operations.
"""

import streamlit as st
from typing import Dict, Any, Optional, List, Callable
import time
import random
from datetime import datetime, timedelta


def render_progress(
    operation: str = "Generating template",
    progress_callback: Optional[Callable] = None,
    estimated_duration: int = 30,
) -> Dict[str, Any]:
    """
    Render a progress indicator for long-running operations.

    Args:
        operation: Description of the current operation
        progress_callback: Optional callback to report progress
        estimated_duration: Estimated duration in seconds

    Returns:
        Progress result dictionary
    """
    st.header("⚡ Processing")

    # Initialize progress state
    if "progress_state" not in st.session_state:
        st.session_state.progress_state = {
            "start_time": datetime.now(),
            "current_step": 0,
            "total_steps": 5,
            "status": "starting",
        }

    progress_state = st.session_state.progress_state

    # Progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    time_remaining = st.empty()
    current_step_text = st.empty()

    # Simulate progress steps
    steps = [
        "Analyzing requirements...",
        "Generating content structure...",
        "Creating database schemas...",
        "Populating sample data...",
        "Finalizing template...",
    ]

    total_steps = len(steps)
    progress_state["total_steps"] = total_steps

    for i, step in enumerate(steps):
        # Update progress
        progress = (i + 1) / total_steps
        progress_bar.progress(progress)

        # Update status
        status_text.text(f"📋 {step}")
        current_step_text.text(f"Step {i + 1} of {total_steps}")

        # Estimate time remaining
        elapsed = datetime.now() - progress_state["start_time"]
        if elapsed.total_seconds() > 0:
            rate = (i + 1) / elapsed.total_seconds()
            remaining_steps = total_steps - (i + 1)
            estimated_remaining = remaining_steps / rate if rate > 0 else 0
            time_remaining.text(f"⏱️ ~{int(estimated_remaining)}s remaining")
        else:
            time_remaining.text(f"⏱️ Estimating time...")

        # Update state
        progress_state["current_step"] = i + 1
        progress_state["status"] = step

        # Call progress callback if provided
        if progress_callback:
            progress_callback(
                {
                    "step": i + 1,
                    "total_steps": total_steps,
                    "progress": progress,
                    "status": step,
                    "elapsed": elapsed.total_seconds(),
                }
            )

        # Simulate processing time
        time.sleep(random.uniform(1.0, 3.0))

    # Complete
    progress_bar.progress(1.0)
    status_text.text("✅ Complete!")
    time_remaining.text("⏱️ Finished")
    current_step_text.text(f"Completed {total_steps} steps")

    # Calculate final stats
    total_time = datetime.now() - progress_state["start_time"]
    result = {
        "success": True,
        "total_time": total_time.total_seconds(),
        "steps_completed": total_steps,
        "completion_time": datetime.now(),
    }

    # Call final callback
    if progress_callback:
        progress_callback(
            {
                "step": total_steps,
                "total_steps": total_steps,
                "progress": 1.0,
                "status": "Complete",
                "elapsed": total_time.total_seconds(),
                "result": result,
            }
        )

    return result


def render_detailed_progress(
    operation: str = "Processing",
    steps: List[str] = None,
    progress_callback: Optional[Callable] = None,
) -> Dict[str, Any]:
    """
    Render a detailed progress indicator with custom steps.

    Args:
        operation: Main operation description
        steps: List of step descriptions
        progress_callback: Optional progress callback

    Returns:
        Progress result dictionary
    """
    if steps is None:
        steps = [
            "Initializing...",
            "Processing data...",
            "Validating results...",
            "Finalizing...",
        ]

    st.subheader(f"⚙️ {operation}")

    # Progress container
    progress_container = st.container()

    with progress_container:
        # Overall progress
        overall_progress = st.progress(0)
        overall_status = st.empty()

        # Step details
        step_progress = st.progress(0)
        step_status = st.empty()
        step_detail = st.empty()

        start_time = datetime.now()
        total_steps = len(steps)

        for i, step in enumerate(steps):
            # Update overall progress
            overall_progress_val = (i) / total_steps
            overall_progress.progress(overall_progress_val)
            overall_status.text(f"Overall: {int(overall_progress_val * 100)}% complete")

            # Step progress simulation
            for sub_step in range(10):  # 10 sub-steps per main step
                step_progress_val = (sub_step + 1) / 10
                step_progress.progress(step_progress_val)
                step_status.text(f"Step {i + 1}/{total_steps}: {step}")
                step_detail.text(f"Sub-step {sub_step + 1}/10: Processing...")

                # Simulate work
                time.sleep(random.uniform(0.1, 0.5))

                # Update overall progress incrementally
                current_overall = (i + step_progress_val / 10) / total_steps
                overall_progress.progress(min(current_overall, 1.0))

            # Call progress callback
            if progress_callback:
                elapsed = datetime.now() - start_time
                progress_callback(
                    {
                        "main_step": i + 1,
                        "total_steps": total_steps,
                        "step_progress": 1.0,
                        "overall_progress": (i + 1) / total_steps,
                        "status": step,
                        "elapsed": elapsed.total_seconds(),
                    }
                )

        # Complete
        overall_progress.progress(1.0)
        overall_status.text("✅ All steps completed!")
        step_progress.progress(1.0)
        step_status.text("Finalizing...")
        step_detail.text("Process complete")

    total_time = datetime.now() - start_time
    return {
        "success": True,
        "total_time": total_time.total_seconds(),
        "steps_completed": total_steps,
        "completion_time": datetime.now(),
    }


def render_progress_with_stages(
    stages: List[Dict[str, Any]], progress_callback: Optional[Callable] = None
) -> Dict[str, Any]:
    """
    Render progress with detailed stages and sub-operations.

    Args:
        stages: List of stage dictionaries with 'name', 'description', 'duration'
        progress_callback: Optional progress callback

    Returns:
        Progress result dictionary
    """
    st.header("🚀 Processing Stages")

    # Calculate total estimated time
    total_estimated = sum(stage.get("duration", 5) for stage in stages)

    # Progress overview
    col1, col2 = st.columns([2, 1])
    with col1:
        overall_progress = st.progress(0)
        overall_status = st.empty()
    with col2:
        time_estimate = st.empty()
        time_estimate.text(f"⏱️ ~{total_estimated}s total")

    start_time = datetime.now()
    completed_stages = 0

    for stage in stages:
        stage_name = stage.get("name", "Processing")
        stage_desc = stage.get("description", "")
        stage_duration = stage.get("duration", 5)

        # Stage header
        with st.expander(
            f"📋 Stage {completed_stages + 1}: {stage_name}", expanded=True
        ):
            st.write(stage_desc)

            # Stage progress
            stage_progress = st.progress(0)
            stage_status = st.empty()

            # Simulate stage work
            for i in range(10):
                progress = (i + 1) / 10
                stage_progress.progress(progress)
                stage_status.text(f"Progress: {int(progress * 100)}%")

                # Update overall progress
                overall_progress_val = (completed_stages + progress) / len(stages)
                overall_progress.progress(overall_progress_val)

                # Update time estimate
                elapsed = datetime.now() - start_time
                remaining_stages = len(stages) - completed_stages - progress
                estimated_remaining = (
                    remaining_stages
                    * (elapsed.total_seconds() / (completed_stages + progress))
                    if (completed_stages + progress) > 0
                    else 0
                )
                time_estimate.text(f"⏱️ ~{int(estimated_remaining)}s remaining")

                time.sleep(stage_duration / 10)

                # Call progress callback
                if progress_callback:
                    progress_callback(
                        {
                            "stage": completed_stages + 1,
                            "total_stages": len(stages),
                            "stage_progress": progress,
                            "overall_progress": overall_progress_val,
                            "stage_name": stage_name,
                            "elapsed": elapsed.total_seconds(),
                        }
                    )

        completed_stages += 1

    # Complete
    overall_progress.progress(1.0)
    overall_status.text("🎉 All stages completed!")

    total_time = datetime.now() - start_time
    return {
        "success": True,
        "total_time": total_time.total_seconds(),
        "stages_completed": len(stages),
        "completion_time": datetime.now(),
    }


def render_template_generation_progress() -> Dict[str, Any]:
    """
    Render progress specifically for template generation.

    Returns:
        Progress result dictionary
    """
    stages = [
        {
            "name": "Analysis",
            "description": "Analyzing your requirements and preferences",
            "duration": 3,
        },
        {
            "name": "Structure",
            "description": "Creating the template structure and layout",
            "duration": 5,
        },
        {
            "name": "Content",
            "description": "Generating content blocks and sample data",
            "duration": 8,
        },
        {
            "name": "Database",
            "description": "Setting up database schemas and properties",
            "duration": 6,
        },
        {
            "name": "Validation",
            "description": "Validating template structure and content",
            "duration": 3,
        },
        {
            "name": "Finalization",
            "description": "Finalizing and preparing for export",
            "duration": 2,
        },
    ]

    return render_progress_with_stages(stages)


def render_spinner_with_message(message: str, duration: float = 2.0):
    """
    Render a simple spinner with message.

    Args:
        message: Message to display
        duration: Duration to show spinner
    """
    with st.spinner(message):
        time.sleep(duration)


def render_progress_metrics(metrics: Dict[str, Any]):
    """
    Render progress metrics in a nice format.

    Args:
        metrics: Dictionary of metrics to display
    """
    st.subheader("📊 Progress Metrics")

    cols = st.columns(len(metrics))

    for i, (key, value) in enumerate(metrics.items()):
        with cols[i]:
            if isinstance(value, float):
                st.metric(key.replace("_", " ").title(), f"{value:.1f}")
            else:
                st.metric(key.replace("_", " ").title(), str(value))


def create_progress_tracker():
    """
    Create a progress tracker instance for manual control.

    Returns:
        ProgressTracker instance
    """
    return ProgressTracker()


class ProgressTracker:
    """Manual progress tracking class."""

    def __init__(self):
        self.start_time = datetime.now()
        self.current_step = 0
        self.total_steps = 0
        self.status = "Initialized"

    def set_total_steps(self, total: int):
        """Set total number of steps."""
        self.total_steps = total

    def update_progress(self, step: int, status: str = ""):
        """Update current progress."""
        self.current_step = step
        if status:
            self.status = status

    def get_progress_info(self) -> Dict[str, Any]:
        """Get current progress information."""
        elapsed = datetime.now() - self.start_time
        progress = self.current_step / self.total_steps if self.total_steps > 0 else 0

        return {
            "current_step": self.current_step,
            "total_steps": self.total_steps,
            "progress": progress,
            "status": self.status,
            "elapsed_seconds": elapsed.total_seconds(),
            "estimated_completion": self._estimate_completion(),
        }

    def _estimate_completion(self) -> Optional[float]:
        """Estimate time to completion."""
        if self.current_step == 0:
            return None

        elapsed = datetime.now() - self.start_time
        rate = self.current_step / elapsed.total_seconds()
        remaining = self.total_steps - self.current_step

        return remaining / rate if rate > 0 else None

    def render_progress_bar(self):
        """Render current progress as a Streamlit progress bar."""
        info = self.get_progress_info()

        progress_bar = st.progress(info["progress"])
        st.text(f"Step {info['current_step']}/{info['total_steps']}: {info['status']}")

        if info["estimated_completion"]:
            st.text(f"Estimated time remaining: {int(info['estimated_completion'])}s")

        return progress_bar


# Export functions
__all__ = [
    "render_progress",
    "render_detailed_progress",
    "render_progress_with_stages",
    "render_template_generation_progress",
    "render_spinner_with_message",
    "render_progress_metrics",
    "create_progress_tracker",
    "ProgressTracker",
]
