# CI/CD Scripts for Code Review Assistant

This directory contains comprehensive CI/CD integration scripts with advanced features including performance metrics, deployment automation, and exit code handling for pipeline integration.

## Scripts Overview

### 1. `deploy.sh` - Production Deployment Script

**Purpose**: Handles production deployments with quality gates and comprehensive error handling.

**Features**:
- Quality gate validation before deployment
- Multi-environment support (staging, production, development)
- Timeout handling for deployments
- Comprehensive exit codes for CI/CD integration
- Deployment verification and rollback capabilities

**Usage**:
```bash
# Basic deployment
./scripts/deploy.sh

# Environment-specific deployment
ENVIRONMENT=production ./scripts/deploy.sh

# Force deployment (bypass quality gates)
FORCE_DEPLOY=true ./scripts/deploy.sh

# Custom timeout
DEPLOYMENT_TIMEOUT=600 ./scripts/deploy.sh
```

**Exit Codes**:
- `0` - Deployment successful
- `1` - General deployment error
- `2` - Quality gate failure (too many critical issues)
- `3` - Configuration error
- `4` - Timeout error
- `5` - Permission/authentication error

**Environment Variables**:
- `ENVIRONMENT` - Target environment (staging/production/development)
- `FORCE_DEPLOY` - Bypass quality gates (true/false)
- `DEPLOYMENT_TIMEOUT` - Timeout in seconds (default: 300)
- `CRITICAL_ISSUE_THRESHOLD` - Max critical issues allowed (default: 5)
- `TOTAL_ISSUE_THRESHOLD` - Max total issues threshold (default: 50)

### 2. `ci-integration.sh` - Universal CI/CD Integration

**Purpose**: Provides standardized CI/CD integration across multiple platforms with performance monitoring.

**Features**:
- Auto-detects CI/CD platform (GitHub Actions, GitLab CI, Jenkins, etc.)
- Platform-specific output formatting
- Cache management
- Quality gate enforcement
- Performance baseline tracking
- Multiple output formats (JSON, JUnit, Prometheus)

**Usage**:
```bash
# Auto-detect CI system
./scripts/ci-integration.sh

# Specify CI system
CI_SYSTEM=github-actions ./scripts/ci-integration.sh

# Custom performance baseline
PERFORMANCE_BASELINE=180 ./scripts/ci-integration.sh

# Enable specific metrics output
METRICS_OUTPUT=prometheus ./scripts/ci-integration.sh
```

**Exit Codes**:
- `0` - Success
- `1` - General failure
- `2` - Quality gate failure
- `3` - Configuration error
- `4` - Performance threshold exceeded
- `5` - Cache/dependency error

**Environment Variables**:
- `CI_SYSTEM` - Force specific CI system detection
- `PERFORMANCE_BASELINE` - Performance threshold in seconds (default: 120)
- `ENABLE_CACHING` - Enable caching support (default: true)
- `METRICS_OUTPUT` - Output format (json/junit/prometheus)

### 3. `performance-monitor.sh` - Advanced Performance Monitoring

**Purpose**: Tracks performance metrics over time, detects regressions, and provides comprehensive reporting.

**Features**:
- Historical performance tracking
- Baseline calculation and comparison
- Performance regression detection
- Multiple report formats (JSON, CSV, HTML, Prometheus)
- Trend analysis
- Alerting for performance degradation

**Usage**:
```bash
# Record performance metrics
./scripts/performance-monitor.sh 120 15 2 45 true github-actions

# Generate performance report
OUTPUT_FORMAT=csv ./scripts/performance-monitor.sh 95 8 0 32

# Custom alert threshold
PERFORMANCE_ALERT_THRESHOLD=15 ./scripts/performance-monitor.sh 140 20 3 50
```

**Parameters**:
1. `execution_time` - Analysis execution time in seconds
2. `total_issues` - Total number of issues found (optional)
3. `critical_issues` - Number of critical issues (optional)
4. `files_analyzed` - Number of files analyzed (optional)
5. `cache_hit` - Whether cache was used (optional)
6. `ci_system` - CI system name (optional)

**Environment Variables**:
- `PERFORMANCE_ALERT_THRESHOLD` - Regression alert threshold in % (default: 20)
- `BASELINE_WINDOW` - Number of runs for baseline (default: 10)
- `OUTPUT_FORMAT` - Report format (json/csv/prometheus/html)

## CI/CD Integration Examples

### GitHub Actions Integration

```yaml
- name: Run Code Review Analysis
  run: |
    # Run your code review analysis here
    python -m src.main --analysis-type=all

- name: CI Integration Check
  run: |
    ./scripts/ci-integration.sh
  env:
    PERFORMANCE_BASELINE: 120
    METRICS_OUTPUT: junit

- name: Deploy to Production
  if: github.ref == 'refs/heads/main' && success()
  run: |
    ./scripts/deploy.sh
  env:
    ENVIRONMENT: production
```

### GitLab CI Integration

```yaml
ci_integration:
  stage: test
  script:
    - ./scripts/ci-integration.sh
  variables:
    CI_SYSTEM: "gitlab-ci"
    PERFORMANCE_BASELINE: "120"
  artifacts:
    reports:
      junit: ci-metrics-junit.xml
      metrics: ci-metrics.json

deploy_production:
  stage: deploy
  script:
    - ./scripts/deploy.sh
  environment:
    name: production
  variables:
    ENVIRONMENT: "production"
  only:
    - main
```

### Jenkins Integration

```groovy
pipeline {
    agent any

    environment {
        CI_SYSTEM = 'jenkins'
        PERFORMANCE_BASELINE = '120'
    }

    stages {
        stage('CI Integration') {
            steps {
                sh './scripts/ci-integration.sh'
            }
            post {
                always {
                    publishTestResults testResultsPattern: 'ci-metrics-junit.xml'
                }
            }
        }

        stage('Deploy') {
            when { branch 'main' }
            steps {
                sh '''
                    export ENVIRONMENT=production
                    ./scripts/deploy.sh
                '''
            }
        }
    }
}
```

## Performance Metrics and Monitoring

### Metrics Collected

- **Execution Time**: Total time for analysis completion
- **Issue Counts**: Total and critical issues found
- **Files Analyzed**: Number of files processed
- **Cache Hit Rate**: Efficiency of caching system
- **Performance Score**: Composite score based on speed and quality

### Performance Baselines

The system automatically calculates performance baselines based on the last 10 successful runs within 30 days. Alerts are triggered when performance degrades beyond the configured threshold (default: 20%).

### Trend Analysis

Performance data is stored in JSON format and can be analyzed for trends:

```bash
# View recent performance trends
cat metrics/performance-report.json | jq '.trends'

# Export to CSV for analysis
OUTPUT_FORMAT=csv ./scripts/performance-monitor.sh 100 10 1 30
```

## Error Handling and Exit Codes

All scripts follow a standardized exit code convention:

- **0**: Success
- **1**: General error
- **2**: Quality gate failure
- **3**: Configuration error
- **4**: Performance/timeout error
- **5**: Permission/authentication error

## File Outputs

### Generated Files

- `deployment-exit-code.txt` - Final deployment exit code
- `ci-exit-code.txt` - CI integration exit code
- `ci-metrics.json` - CI performance metrics
- `quality-gate-report.json` - Quality assessment results
- `performance-metrics.json` - Performance data for monitoring systems
- `metrics/performance-history.json` - Historical performance data
- `metrics/performance-baseline.json` - Performance baseline calculations

### Log Files

- `deployment.log` - Deployment activity log
- `ci-integration.log` - CI integration log
- `performance.log` - Performance monitoring log

## Security Considerations

- All scripts validate input parameters
- Secrets should be passed via environment variables, not command line
- Scripts include proper error handling to prevent information leakage
- File permissions are set to executable only for the owner

## Troubleshooting

### Common Issues

1. **Permission Denied**: Ensure scripts are executable (`chmod +x scripts/*.sh`)
2. **Missing Dependencies**: Install required tools (jq, python3, git)
3. **Configuration Errors**: Validate that required files exist before running
4. **Performance Alerts**: Check baseline calculations and adjust thresholds if needed

### Debug Mode

Enable debug output by setting:
```bash
export DEBUG=true
./scripts/deploy.sh
```

## Contributing

When adding new features to these scripts:

1. Follow the existing exit code conventions
2. Add comprehensive error handling
3. Update this documentation
4. Test with multiple CI/CD systems
5. Ensure backward compatibility

For questions or issues, please refer to the main project documentation or create an issue in the project repository.