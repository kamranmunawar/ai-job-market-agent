
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from job_title_matcher import JobTitleMatcherTool


matcher = JobTitleMatcherTool()

assert matcher.is_match(
    "AI Engineer - SC Cleared",
    "AI Engineer &amp;#8211; SC Cleared"
)

assert matcher.is_match(
    "AI Engineer - SC Cleared",
    "AI Engineer – SC Cleared"
)

assert not matcher.is_match(
    "Core AI Engineer",
    "Applied AI Engineer"
)

print("PASS: Double-encoded HTML title")
print("PASS: Unicode dash normalisation")
print("PASS: Different job titles still rejected")
print("\nALL TITLE NORMALISATION TESTS PASSED")
