
def should_process(status: str | None) -> bool:
    return status not in ("completed", "needs_review")


def main():
    cases = [
        (None, True),
        ("completed", False),
        ("needs_review", False),
        ("failed", True),
    ]

    for status, expected in cases:
        actual = should_process(status)

        assert actual == expected, (
            f"Status {status}: expected {expected}, got {actual}"
        )

        print(f"PASS: {status} -> process={actual}")


if __name__ == "__main__":
    main()
