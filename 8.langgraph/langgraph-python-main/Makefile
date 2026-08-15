.PHONY: debug course course-push

debug:
	langgraph dev --debug-port 5678

course:
	uv run python scripts/course.py

course-push:
	@[ -n "$(SHA)" ] || (echo "请提供提交 hash: make course-push SHA=<hash>" && exit 1)
	uv run python scripts/course-push.py $(SHA)
