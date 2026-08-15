#!/usr/bin/env python3
"""交互式选择带编号的提交并切换到对应分支。"""

import re
import subprocess
import sys

import questionary
from questionary import Style
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

CUSTOM_STYLE = Style(
    [
        ("qmark", "fg:#ff5f87 bold"),
        ("question", "fg:#e0e0e0 bold"),
        ("answer", "fg:#5f87ff bold"),
        ("pointer", "fg:#ff5f00 bold"),
        ("highlighted", "fg:#ffffff bg:#5f87ff bold"),
        ("selected", "fg:#5f87ff"),
        ("separator", "fg:#444444"),
        ("instruction", "fg:#666666 italic"),
    ]
)


def get_commits() -> list[dict]:
    result = subprocess.run(
        ["git", "log", "--format=%H;%s"],
        capture_output=True,
        text=True,
    )
    commits: list[dict] = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split(";", 1)
        if len(parts) != 2:
            continue
        m = re.match(r"^(\d+)\.\s*(.*)", parts[1])
        if m:
            commits.append(
                {
                    "hash": parts[0],
                    "number": m.group(1),
                    "message": m.group(2),
                }
            )
    return commits


def get_current_head() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def get_current_branch() -> str:
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def checkout(number: str, commit_hash: str) -> None:
    r = subprocess.run(
        ["git", "branch", "--list", number],
        capture_output=True,
        text=True,
    )
    if r.stdout.strip():
        subprocess.run(["git", "checkout", number], check=True)
    else:
        subprocess.run(["git", "checkout", "-b", number, commit_hash], check=True)


def switch_course() -> None:
    commits = get_commits()

    if not commits:
        console.print(
            Panel(
                "[bold]没有找到 message 格式为「数字. 消息」的提交[/]",
                title=":warning:  提示",
                border_style="red",
            )
        )
        return

    current_head = get_current_head()
    has_current = any(c["hash"] == current_head for c in commits)

    header = Text()
    header.append("课程分支切换\n", style="bold white")
    header.append(f"共发现 ", style="dim")
    header.append(f"{len(commits)}", style="bold cyan")
    header.append(f" 个课程提交", style="dim")
    if has_current:
        current_number = next(c["number"] for c in commits if c["hash"] == current_head)
        header.append(f"  |  当前: ", style="dim")
        header.append(current_number, style="bold green")
    console.print(Panel(header, border_style="cyan"))
    console.print()

    choices = [
        questionary.Choice(
            title=(
                f"{'●' if c['hash'] == current_head else ' '} "
                f"{c['number']:<6} {c['message'][:56]}{'…' if len(c['message']) > 56 else ''}"
            ),
            value=c,
        )
        for c in commits
    ]

    selected = questionary.select(
        "请选择要切换到的课程提交",
        choices=choices,
        style=CUSTOM_STYLE,
        use_shortcuts=True,
    ).ask()

    if selected is None:
        console.print("\n[dim]已取消[/]")
        return

    checkout(selected["number"], selected["hash"])
    console.print()
    console.print(
        Panel(
            f"[bold green]{selected['number']}[/]\n[dim]{selected['message']}[/]",
            title=":white_check_mark:  切换成功",
            border_style="green",
        )
    )


def update_courses() -> None:
    console.print(Panel("更新资料", style="bold white", border_style="cyan"))
    console.print()

    # 1. fetch
    console.print("[dim]正在从服务器拉取最新数据…[/]")
    fetch_result = subprocess.run(
        ["git", "fetch", "origin"],
        capture_output=True,
        text=True,
    )
    if fetch_result.returncode != 0:
        console.print(
            Panel(
                f"[bold red]拉取失败[/]\n[dim]{fetch_result.stderr.strip()}[/]",
                border_style="red",
            )
        )
        return

    # 2. 检查 origin/main 是否存在
    origin_rev = subprocess.run(
        ["git", "rev-parse", "origin/main"],
        capture_output=True,
        text=True,
    )
    if origin_rev.returncode != 0:
        console.print(
            Panel(
                "[bold red]远程分支 origin/main 不存在[/]",
                border_style="red",
            )
        )
        return
    origin_head = origin_rev.stdout.strip()

    # 3. 检查本地 main 是否存在
    local_rev = subprocess.run(
        ["git", "rev-parse", "main"],
        capture_output=True,
        text=True,
    )
    local_main_exists = local_rev.returncode == 0
    local_head = local_rev.stdout.strip() if local_main_exists else None

    # 4. 已是最新
    if local_main_exists and local_head == origin_head:
        console.print(
            Panel(
                "[green]本地 main 已与服务器一致，无需更新[/]",
                border_style="green",
            )
        )
        return

    # 5. 判断能否快进
    current_branch = get_current_branch()

    if local_main_exists:
        ff_check = subprocess.run(
            ["git", "merge-base", "--is-ancestor", "main", "origin/main"],
            capture_output=True,
        )
        can_ff = ff_check.returncode == 0
    else:
        can_ff = False

    if can_ff:
        console.print("[dim]服务器有新提交，执行快进…[/]")
        if current_branch != "main":
            subprocess.run(
                ["git", "checkout", "main"],
                check=True,
                capture_output=True,
            )
        subprocess.run(
            ["git", "merge", "--ff-only", "origin/main"],
            check=True,
            capture_output=True,
        )
        console.print(
            Panel(
                "[bold green]main 已快进到最新[/]",
                title=":white_check_mark:  更新完成",
                border_style="green",
            )
        )
        return

    # 6. 无法快进 —— 强制同步

    console.print("[dim]分支历史不一致，正在强制同步…[/]")

    # 7. 执行强制更新
    # 先 detach，以免当前分支被删除时报错
    subprocess.run(
        ["git", "checkout", "--detach", "--force", "origin/main"],
        check=True,
        capture_output=True,
    )

    # 删除除 main 外的所有本地分支
    branches_result = subprocess.run(
        ["git", "for-each-ref", "refs/heads/", "--format=%(refname:short)"],
        capture_output=True,
        text=True,
        check=True,
    )
    for branch in branches_result.stdout.strip().split("\n"):
        if branch and branch != "main":
            subprocess.run(
                ["git", "branch", "-D", branch],
                check=True,
                capture_output=True,
            )

    # 强制将 main 指向 origin/main 并切过去
    subprocess.run(
        ["git", "checkout", "-B", "main", "origin/main"],
        check=True,
        capture_output=True,
    )

    console.print(
        Panel(
            "[bold green]main 已强制同步到服务器版本，其余分支已全部删除[/]",
            title=":white_check_mark:  强制更新完成",
            border_style="green",
        )
    )


def main() -> None:
    action = questionary.select(
        "请选择操作",
        choices=[
            questionary.Choice("切换资料", value="switch"),
            questionary.Choice("更新资料", value="update"),
        ],
        style=CUSTOM_STYLE,
    ).ask()

    if action is None:
        console.print("\n[dim]已取消[/]")
        sys.exit(0)
    elif action == "switch":
        switch_course()
    elif action == "update":
        update_courses()


if __name__ == "__main__":
    main()
