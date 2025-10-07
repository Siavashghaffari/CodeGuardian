#!/usr/bin/env python3
"""
Output Formatters Examples

Demonstrates how to use the various output formatters and notification systems.
"""

import asyncio
from pathlib import Path
from datetime import datetime

from src.formatters import (
    create_formatter, create_output_router, create_template_formatter,
    FormatterConfig, OutputContext, OutputRequest,
    NotificationManager, NotificationConfig
)
from src.config.rule_engine import RuleResult
from src.config.schema import SeverityLevel


def create_sample_results():
    """Create sample results for demonstration."""
    sample_results = [
        RuleResult(
            rule_name="hardcoded_secrets",
            checker_name="security",
            severity=SeverityLevel.ERROR,
            message="Hardcoded API key found",
            file_path=Path("src/config/settings.py"),
            line_number=42,
            column=15,
            suggestion="Use environment variables for API keys"
        ),
        RuleResult(
            rule_name="max_function_length",
            checker_name="complexity",
            severity=SeverityLevel.WARNING,
            message="Function too long (65 lines)",
            file_path=Path("src/analyzer/parser.py"),
            line_number=120,
            suggestion="Consider breaking this function into smaller functions"
        ),
        RuleResult(
            rule_name="unused_variable",
            checker_name="variables",
            severity=SeverityLevel.SUGGESTION,
            message="Variable 'temp_data' is defined but never used",
            file_path=Path("src/utils/helper.py"),
            line_number=28,
            column=8,
            suggestion="Remove unused variable or use it"
        )
    ]
    return sample_results


def demonstrate_terminal_formatter():
    """Demonstrate terminal formatter."""
    print("=== Terminal Formatter Demo ===\n")

    results = create_sample_results()
    config = FormatterConfig(show_suggestions=True, show_line_numbers=True)
    context = OutputContext(
        analysis_type="files",
        files_analyzed=10,
        timestamp=datetime.now()
    )

    # Create terminal formatter
    terminal_formatter = create_formatter("terminal", config, context)

    # Format detailed output
    detailed_output = terminal_formatter.format(results, sub_format="detailed")
    print("Detailed Format:")
    print(detailed_output.content)
    print("\n" + "="*50 + "\n")

    # Format compact output
    compact_output = terminal_formatter.format(results, sub_format="compact")
    print("Compact Format:")
    print(compact_output.content)
    print("\n" + "="*50 + "\n")


def demonstrate_markdown_formatter():
    """Demonstrate markdown formatter."""
    print("=== Markdown Formatter Demo ===\n")

    results = create_sample_results()
    config = FormatterConfig(show_suggestions=True, include_metadata=True)
    context = OutputContext(
        analysis_type="pull_request",
        repository_url="https://github.com/example/repo",
        files_analyzed=10
    )

    # Create markdown formatter
    markdown_formatter = create_formatter("markdown", config, context)

    # Format for GitHub PR comment
    pr_comment = markdown_formatter.format(results, sub_format="pr_comment")
    print("PR Comment Format:")
    print(pr_comment.content)
    print("\n" + "="*50 + "\n")


def demonstrate_json_formatter():
    """Demonstrate JSON formatter."""
    print("=== JSON Formatter Demo ===\n")

    results = create_sample_results()
    config = FormatterConfig(include_metadata=True)
    context = OutputContext(
        analysis_type="ci_cd",
        repository_url="https://github.com/example/repo",
        files_analyzed=10,
        execution_time=2.5
    )

    # Create JSON formatter
    json_formatter = create_formatter("json", config, context)

    # Format for GitLab CI
    gitlab_output = json_formatter.format(results, sub_format="gitlab_ci")
    print("GitLab CI Format:")
    print(gitlab_output.content[:500] + "...")
    print("\n" + "="*50 + "\n")

    # Format for metrics
    metrics_output = json_formatter.format(results, sub_format="metrics")
    print("Metrics Format (truncated):")
    print(metrics_output.content[:500] + "...")
    print("\n" + "="*50 + "\n")


def demonstrate_template_formatter():
    """Demonstrate template formatter."""
    print("=== Template Formatter Demo ===\n")

    results = create_sample_results()
    config = FormatterConfig(show_suggestions=True)
    context = OutputContext(
        repository_url="https://github.com/example/repo",
        files_analyzed=10
    )

    # Create template formatter
    template_formatter = create_template_formatter("summary_only", config, context)

    # Format using built-in template
    summary_output = template_formatter.format(results, template_name="summary_only")
    print("Summary Template:")
    print(summary_output.content)
    print("\n" + "="*50 + "\n")

    # Custom template
    custom_template = """
# Custom Report

Found {{ summary.total_issues }} issues in {{ summary.files_analyzed }} files.

{% if results %}
Top Issues:
{% for result in results %}
{{ loop.index }}. {{ result.severity | upper }}: {{ result.message }}
{% endfor %}
{% endif %}

Status: {% if summary.total_issues == 0 %}✅ Clean{% else %}⚠️ Needs Review{% endif %}
    """.strip()

    custom_output = template_formatter.format(
        results,
        template_name="custom",
        template_content=custom_template
    )
    print("Custom Template:")
    print(custom_output.content)
    print("\n" + "="*50 + "\n")


async def demonstrate_output_router():
    """Demonstrate output router with multiple formats."""
    print("=== Output Router Demo ===\n")

    results = create_sample_results()
    context = OutputContext(
        analysis_type="batch",
        repository_url="https://github.com/example/repo",
        files_analyzed=10
    )

    # Create output router
    router = create_output_router()

    # Prepare multiple output requests
    requests = [
        OutputRequest(
            format_type="terminal",
            sub_format="compact",
            results=results,
            context=context
        ),
        OutputRequest(
            format_type="markdown",
            sub_format="github",
            results=results,
            context=context
        ),
        OutputRequest(
            format_type="json",
            sub_format="sarif",
            results=results,
            context=context
        )
    ]

    # Format multiple outputs in parallel
    responses = await router.format_multiple(requests)

    for i, response in enumerate(responses):
        if response.success:
            print(f"Response {i+1} - {response.metadata.get('formatter', 'unknown')} format:")
            print(f"Size: {response.formatted_output.size_bytes} bytes")
            print(f"Content preview: {response.formatted_output.content[:100]}...")
        else:
            print(f"Response {i+1} failed: {response.error}")
        print()


async def demonstrate_notifications():
    """Demonstrate notification system."""
    print("=== Notification System Demo ===\n")

    results = create_sample_results()
    context = OutputContext(
        analysis_type="pull_request",
        repository_url="https://github.com/example/repo",
        pr_number=123,
        files_analyzed=10
    )

    # Configure notifications (using dummy URLs)
    notification_config = NotificationConfig(
        enabled=True,
        webhook_url="https://hooks.slack.com/services/dummy/webhook/url",
        severity_threshold="warning",
        max_issues_in_notification=5,
        mention_users=["@developer", "@team-lead"]
    )

    # Create notification manager
    notification_manager = NotificationManager(notification_config)

    # This would normally send real notifications
    print("Notification configuration:")
    print(f"- Enabled: {notification_config.enabled}")
    print(f"- Severity threshold: {notification_config.severity_threshold}")
    print(f"- Max issues: {notification_config.max_issues_in_notification}")
    print(f"- Webhook URL: {notification_config.webhook_url[:50]}...")
    print("\n(Notifications would be sent to Slack, Teams, etc.)")
    print("\n" + "="*50 + "\n")


def demonstrate_html_dashboard():
    """Demonstrate HTML dashboard."""
    print("=== HTML Dashboard Demo ===\n")

    results = create_sample_results()
    config = FormatterConfig(show_suggestions=True, include_metadata=True)
    context = OutputContext(
        analysis_type="dashboard",
        repository_url="https://github.com/example/repo",
        files_analyzed=10,
        execution_time=3.2
    )

    # Create HTML formatter
    html_formatter = create_formatter("html", config, context)

    # Format dashboard
    dashboard_output = html_formatter.format(results, sub_format="dashboard", theme="default")
    print("HTML Dashboard created!")
    print(f"Size: {dashboard_output.size_bytes} bytes")
    print("Features: Interactive charts, filtering, responsive design")

    # Save to file (optional)
    dashboard_path = Path("dashboard_example.html")
    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(dashboard_output.content)
    print(f"Dashboard saved to: {dashboard_path}")
    print("\n" + "="*50 + "\n")


async def main():
    """Run all demonstrations."""
    print("🔍 Code Review Output Formatters Demo\n")
    print("This script demonstrates the various output formatters available.\n")

    # Terminal formatter
    demonstrate_terminal_formatter()

    # Markdown formatter
    demonstrate_markdown_formatter()

    # JSON formatter
    demonstrate_json_formatter()

    # Template formatter
    demonstrate_template_formatter()

    # Output router (async)
    await demonstrate_output_router()

    # Notification system (async)
    await demonstrate_notifications()

    # HTML dashboard
    demonstrate_html_dashboard()

    print("🎉 Demo completed!")
    print("\nAll formatters are ready for integration with your code review workflow!")


if __name__ == "__main__":
    asyncio.run(main())