# Contributing to McGuardian Elite

🎉 Thank you for your interest in contributing to McGuardian Elite! We welcome contributions from security professionals, developers, and enthusiasts who want to help make Mac security better for everyone.

## 🌟 Ways to Contribute

### 🐛 Bug Reports
- Report security vulnerabilities responsibly (see [Security Policy](#-security-policy))
- Submit detailed bug reports with reproduction steps
- Help triage and verify existing issues

### 💡 Feature Requests  
- Propose new security monitoring capabilities
- Suggest UI/UX improvements
- Request new threat intelligence integrations

### 🔧 Code Contributions
- Fix bugs and implement features
- Improve performance and efficiency
- Add new threat detection algorithms
- Enhance the web dashboard

### 📖 Documentation
- Improve installation instructions
- Write security best practices guides
- Create video tutorials
- Translate documentation

### 🧪 Testing
- Test on different macOS versions
- Validate security detections
- Performance testing and optimization
- Accessibility testing

## 🚀 Getting Started

### Prerequisites

- **macOS 10.15+** (Catalina or later)
- **Python 3.8+** with pip
- **Git** for version control
- **Basic security knowledge** (recommended)

### Development Setup

1. **Fork the Repository**
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/yourusername/mcguardian-elite.git
   cd mcguardian-elite
   ```

2. **Set Up Development Environment**
   ```bash
   # Run the Python installer for development setup
   python3 mcguardian_installer.py
   
   # Or create virtual environment manually
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run Tests**
   ```bash
   # Run unit tests
   pytest tests/
   
   # Run security tests
   pytest tests/security/
   
   # Run integration tests
   pytest tests/integration/
   ```

4. **Start Development Server**
   ```bash
   # Start the security engine
   python3 mcguardian_pro.py
   
   # In another terminal, start dashboard
   python3 mcguardian_gui.py
   ```

**Note about Installation Files:**
- **`install.sh`** - Quick curl-based installer for end users
- **`mcguardian_installer.py`** - Main Python installer that does the comprehensive setup

## 📋 Contribution Guidelines

### 🎯 Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-new-feature
   ```

2. **Make Your Changes**
   - Write clean, documented code
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Test Thoroughly**
   ```bash
   # Run all tests
   pytest
   
   # Check code formatting
   black --check .
   
   # Run linting
   flake8 .
   
   # Type checking
   mypy .
   ```

4. **Commit with Clear Messages**
   ```bash
   git commit -m "feat: add advanced behavioral analysis engine
   
   - Implements machine learning-based threat detection
   - Adds support for anomaly detection algorithms
   - Includes comprehensive test suite
   - Updates documentation with new features"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/amazing-new-feature
   ```

### 📝 Commit Message Convention

We use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

**Examples:**
```
feat(dashboard): add real-time threat visualization
fix(monitor): resolve file watching memory leak
docs(readme): update installation instructions
test(security): add penetration testing scenarios
```

### 🎨 Code Style

We follow Python best practices and maintain consistency:

**Python Code Style:**
```python
# Use type hints
def analyze_threat(event: ThreatEvent) -> ThreatAssessment:
    """Analyze threat event and return assessment.
    
    Args:
        event: The security event to analyze
        
    Returns:
        Comprehensive threat assessment
        
    Raises:
        ValueError: If event data is invalid
    """
    pass

# Use descriptive variable names
threat_risk_score = calculate_risk_score(event_data)
is_suspicious_activity = threat_risk_score > RISK_THRESHOLD

# Follow PEP 8 guidelines
class ThreatAnalyzer:
    """Advanced threat analysis engine."""
    
    def __init__(self, config: Dict[str, Any]) -> None:
        self.config = config
        self.threat_patterns = load_threat_patterns()
```

**Frontend Code Style:**
```javascript
// Use modern JavaScript features
const analyzeSecurityEvent = async (eventData) => {
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(eventData)
        });
        
        return await response.json();
    } catch (error) {
        console.error('Security analysis failed:', error);
        throw error;
    }
};

// Use meaningful function names
const updateThreatVisualization = (threatData) => {
    // Implementation
};
```

### 🧪 Testing Requirements

All contributions must include appropriate tests:

**Unit Tests:**
```python
import pytest
from mcguardian.analyzer import ThreatAnalyzer

class TestThreatAnalyzer:
    def test_analyze_malicious_process(self):
        """Test detection of known malicious processes."""
        analyzer = ThreatAnalyzer()
        event = create_process_event("nc", ["-l", "1337"])
        
        result = analyzer.analyze_process_behavior(event)
        
        assert result.risk_score >= 70
        assert "network utility" in result.risk_factors
        
    def test_false_positive_prevention(self):
        """Ensure legitimate processes aren't flagged."""
        analyzer = ThreatAnalyzer()
        event = create_process_event("python3", ["manage.py", "runserver"])
        
        result = analyzer.analyze_process_behavior(event)
        
        assert result.risk_score < 30
```

**Integration Tests:**
```python
@pytest.mark.integration
def test_full_detection_pipeline():
    """Test complete threat detection workflow."""
    # Create test scenario
    with create_test_environment() as env:
        # Trigger security event
        env.execute_command("nmap localhost")
        
        # Wait for detection
        time.sleep(2)
        
        # Verify detection
        events = env.get_security_events()
        assert len(events) > 0
        assert any("nmap" in event.description for event in events)
```

### 📚 Documentation Standards

**Code Documentation:**
```python
class ThreatIntelligence:
    """Comprehensive threat intelligence and analysis system.
    
    This class provides advanced threat detection capabilities including:
    - Behavioral analysis of processes and network connections
    - Pattern recognition for multi-stage attacks
    - Risk scoring and threat categorization
    - Integration with external threat intelligence feeds
    
    Attributes:
        config: Configuration dictionary with analysis parameters
        threat_patterns: Database of known attack patterns
        ml_model: Machine learning model for behavioral analysis
        
    Example:
        >>> intel = ThreatIntelligence(config)
        >>> assessment = intel.analyze_event(security_event)
        >>> if assessment.risk_score > 70:
        ...     handle_high_risk_threat(assessment)
    """
```

**API Documentation:**
```python
@app.route('/api/threats/<threat_id>', methods=['GET'])
def get_threat_details(threat_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific threat.
    
    Args:
        threat_id: Unique identifier for the threat
        
    Returns:
        Dictionary containing:
        - threat_info: Basic threat information
        - risk_assessment: Risk score and factors
        - countermeasures: Recommended actions
        - timeline: Event timeline if available
        
    Raises:
        404: Threat not found
        400: Invalid threat ID format
        
    Example:
        GET /api/threats/threat_123456789
        
        {
            "threat_info": {
                "id": "threat_123456789",
                "type": "lateral_movement",
                "severity": "high"
            },
            "risk_assessment": {
                "score": 85,
                "factors": ["ssh_brute_force", "privilege_escalation"]
            }
        }
    """
```

## 🔒 Security Policy

### Reporting Security Vulnerabilities

**🚨 DO NOT create public issues for security vulnerabilities**

Instead:

1. **Email:** security@mcguardian.dev
2. **Include:**
   - Detailed description of the vulnerability
   - Steps to reproduce
   - Potential impact assessment
   - Suggested mitigation (if any)

3. **Response Time:**
   - Initial response: 24 hours
   - Detailed analysis: 72 hours
   - Fix timeline: Depends on severity

### Security Review Process

All security-related contributions undergo additional review:

1. **Automated Security Scanning**
   - Dependency vulnerability checks
   - Static code analysis
   - Security linting

2. **Manual Security Review**
   - Threat model assessment
   - Attack surface analysis
   - Privilege escalation checks

3. **Penetration Testing**
   - Internal security team testing
   - External security audit (for major changes)

## 🏷️ Issue Labels

We use labels to organize and prioritize issues:

### Priority
- `priority/critical` - Security vulnerabilities, system crashes
- `priority/high` - Important features, significant bugs
- `priority/medium` - Standard features and improvements
- `priority/low` - Nice-to-have features, minor issues

### Type
- `type/bug` - Something isn't working correctly
- `type/feature` - New functionality request
- `type/enhancement` - Improvement to existing functionality
- `type/documentation` - Documentation improvements
- `type/question` - General questions or clarifications

### Component
- `component/security-engine` - Core security monitoring
- `component/dashboard` - Web interface
- `component/installer` - Installation system
- `component/ai-analysis` - AI/ML threat detection
- `component/api` - REST API endpoints

### Status
- `status/triage` - Needs initial review and prioritization
- `status/accepted` - Approved for implementation
- `status/in-progress` - Currently being worked on
- `status/blocked` - Waiting for external dependency
- `status/needs-info` - Requires additional information

## 🎖️ Recognition

We value all contributions and recognize them in several ways:

### Contributors Hall of Fame
- Listed in README.md
- Special Discord role
- Invitation to exclusive contributor events

### Contribution Types
- 🔧 **Core Contributors** - Major features and architecture
- 🐛 **Bug Hunters** - Bug reports and fixes
- 📖 **Documentation Heroes** - Documentation improvements
- 🧪 **Quality Guardians** - Testing and quality assurance
- 🎨 **Design Artists** - UI/UX improvements
- 🛡️ **Security Experts** - Security reviews and improvements

## 📞 Getting Help

### Community Support
- 💬 [Discord Server](https://discord.gg/mcguardian-elite)
- 🗨️ [GitHub Discussions](https://github.com/yourusername/mcguardian-elite/discussions)
- 📧 [Community Forum](https://community.mcguardian.dev)

### Development Help
- 📖 [Developer Documentation](https://docs.mcguardian.dev/development)
- 🎥 [Development Tutorials](https://youtube.com/mcguardian-dev)
- 💻 [Code Examples](https://github.com/yourusername/mcguardian-examples)

### Mentorship Program
New to open source or security? We offer mentorship:
- Pair programming sessions
- Code review guidance
- Security concepts education
- Career development advice

Contact: mentorship@mcguardian.dev

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of:
- Age, body size, disability, ethnicity
- Gender identity and expression
- Level of experience, education, socio-economic status
- Nationality, personal appearance, race, religion
- Sexual identity and orientation

### Our Standards

**Positive behaviors:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what's best for the community
- Showing empathy towards other community members

**Unacceptable behaviors:**
- Trolling, insulting/derogatory comments, personal attacks
- Public or private harassment
- Publishing others' private information without permission
- Conduct which could reasonably be considered inappropriate

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported to: conduct@mcguardian.dev

All complaints will be reviewed and investigated promptly and fairly.

## ⚖️ Legal Considerations

### Intellectual Property
- By contributing, you agree to license your contributions under the MIT License
- Ensure you have rights to contribute any code or content
- Don't include copyrighted material without proper license

### Export Control
- Be aware of export control laws that may apply to security software
- Don't contribute code that violates export restrictions
- Consider international implications of security features

### Responsible Disclosure
- Don't include exploit code or detailed vulnerability information
- Focus on defensive capabilities rather than offensive tools
- Consider the dual-use nature of security technologies

---

## 🎉 Thank You!

Your contributions make McGuardian Elite better for the entire security community. Whether you're fixing a typo, adding a major feature, or helping other users, every contribution matters.

**Happy coding, and stay secure! 🛡️**

---

<div align="center">

**Questions?** Join our [Discord](https://discord.gg/mcguardian-elite) or open a [Discussion](https://github.com/yourusername/mcguardian-elite/discussions)

[🏠 Back to README](README.md) • [📖 Documentation](https://docs.mcguardian.dev) • [🐛 Report Issue](https://github.com/yourusername/mcguardian-elite/issues)

</div>
