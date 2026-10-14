
MAX_RETRIES = 3


def should_process(status: str | None, retry_count: int) -> bool:
    if status in ("completed", "needs_review"):
        return False

    if status == "failed" and retry_count >= MAX_RETRIES:
        return False

    return True


def main():
    cases = [
        (None, 0, True),
        ("completed", 0, False),
        ("needs_review", 0, False),
        ("failed", 0, True),
        ("failed", 1, True),
        ("failed", 2, True),
        ("failed", 3, False),
        ("failed", 4, False),
    ]

    for status, count, expected in cases:
        actual = should_process(status, count)

        assert actual == expected, (
            f"Status={status}, retries={count}: "
            f"expected {expected}, got {actual}"
        )

        print(
            f"PASS: status={status}, "
            f"retries={count}, process={actual}"
        )


if __name__ == "__main__":
    main()
