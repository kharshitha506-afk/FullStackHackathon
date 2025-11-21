import re
from urllib.parse import urlparse


def check_rules(text):
    """
    Rule-based phishing detection engine.
    Returns a list of triggered rules with severity.
    """
    rules_triggered = []
    text_lower = text.lower()

    urgent_keywords = [
        'urgent', 'immediately', 'act now', 'limited time', 'expires',
        'expire', 'suspended', 'locked', 'verify now', 'within 24 hours',
        'final notice', 'last chance'
    ]

    money_keywords = [
        'win', 'won', 'winner', 'prize', 'claim', 'free', 'inheritance',
        'refund', 'reward', '$', 'million', 'thousand', 'loan', 'approved',
        'grant'
    ]

    threat_keywords = [
        'suspended', 'locked', 'closed', 'terminated', 'arrest',
        'legal action', 'compromised', 'breach', 'unauthorized',
        'security alert'
    ]

    impersonation_keywords = [
        'bank', 'paypal', 'amazon', 'netflix', 'apple', 'microsoft', 'google',
        'irs', 'social security', 'government', 'customs'
    ]

    for keyword in urgent_keywords:
        if keyword in text_lower:
            rules_triggered.append({
                'rule': 'Urgency Detected',
                'detail': f'Contains urgency keyword: "{keyword}"',
                'severity': 'high'
            })
            break

    for keyword in money_keywords:
        if keyword in text_lower:
            rules_triggered.append({
                'rule': 'Money/Prize Mention',
                'detail': f'Contains money-related keyword: "{keyword}"',
                'severity': 'medium'
            })
            break

    for keyword in threat_keywords:
        if keyword in text_lower:
            rules_triggered.append({
                'rule': 'Threatening Language',
                'detail': f'Contains threat keyword: "{keyword}"',
                'severity': 'high'
            })
            break

    for keyword in impersonation_keywords:
        if keyword in text_lower:
            rules_triggered.append({
                'rule': 'Brand Impersonation',
                'detail': f'Mentions brand/organization: "{keyword}"',
                'severity': 'medium'
            })
            break

    url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls = re.findall(url_pattern, text)

    suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top']
    for url in urls:
        for tld in suspicious_tlds:
            if tld in url:
                rules_triggered.append({
                    'rule': 'Suspicious URL',
                    'detail': f'URL contains suspicious domain: {url}',
                    'severity': 'high'
                })
                break

    if len(urls) > 3:
        rules_triggered.append({
            'rule': 'Multiple Links',
            'detail': f'Contains {len(urls)} links (suspicious)',
            'severity': 'medium'
        })

    return rules_triggered


def detect_psychology_triggers(text):
    """
    Detect psychological manipulation tactics.
    Returns identified triggers with explanations.
    """
    triggers = []
    text_lower = text.lower()

    urgency_patterns = [
        'urgent', 'immediately', 'now', 'expire', 'expires', 'limited time',
        'act fast', 'hurry', 'last chance', 'within 24 hours', 'final notice'
    ]

    fear_patterns = [
        'suspended', 'locked', 'closed', 'terminated', 'arrest',
        'legal action', 'compromised', 'breach', 'lose access',
        'account closure', 'security alert', 'unauthorized'
    ]

    authority_patterns = [
        'bank', 'irs', 'government', 'police', 'microsoft', 'apple', 'amazon',
        'official', 'department', 'security team'
    ]

    reward_patterns = [
        'win', 'won', 'winner', 'prize', 'free', 'congratulations', 'selected',
        'approved', 'reward', 'gift', 'inheritance'
    ]

    if any(pattern in text_lower for pattern in urgency_patterns):
        triggers.append({
            'type':
            'Urgency',
            'description':
            'Creates pressure to act quickly without thinking',
            'tactic':
            'Time pressure to bypass rational decision-making'
        })

    if any(pattern in text_lower for pattern in fear_patterns):
        triggers.append({
            'type':
            'Fear',
            'description':
            'Uses threats or scary consequences',
            'tactic':
            'Emotional manipulation through anxiety and panic'
        })

    if any(pattern in text_lower for pattern in authority_patterns):
        triggers.append({
            'type': 'Authority',
            'description': 'Impersonates trusted organizations',
            'tactic': 'Exploits trust in legitimate institutions'
        })

    if any(pattern in text_lower for pattern in reward_patterns):
        triggers.append({
            'type':
            'Reward',
            'description':
            'Promises unrealistic gains or prizes',
            'tactic':
            'Greed exploitation with too-good-to-be-true offers'
        })

    return triggers


def analyze_url(url):
    """
    Analyze URL for phishing indicators.
    Returns safety checks and warnings.
    """
    checks = []

    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()

        if not parsed.scheme:
            checks.append({
                'check': 'Protocol Check',
                'status': 'warning',
                'message': 'No protocol specified (http/https)'
            })
        elif parsed.scheme == 'http':
            checks.append({
                'check': 'HTTPS Check',
                'status': 'warning',
                'message': 'Not using secure HTTPS connection'
            })
        else:
            checks.append({
                'check': 'HTTPS Check',
                'status': 'safe',
                'message': 'Uses secure HTTPS connection'
            })

        suspicious_tlds = [
            '.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.zip'
        ]
        if any(domain.endswith(tld) for tld in suspicious_tlds):
            checks.append({
                'check':
                'Domain TLD',
                'status':
                'danger',
                'message':
                'Suspicious top-level domain commonly used in scams'
            })
        else:
            checks.append({
                'check': 'Domain TLD',
                'status': 'safe',
                'message': 'Standard top-level domain'
            })

        if '@' in domain or '@' in url:
            checks.append({
                'check':
                'URL Format',
                'status':
                'danger',
                'message':
                'Contains @ symbol (potential obfuscation)'
            })

        if domain.count('.') > 3:
            checks.append({
                'check':
                'Subdomain Check',
                'status':
                'warning',
                'message':
                f'Excessive subdomains detected ({domain.count(".")} dots)'
            })

        if len(domain) > 40:
            checks.append({
                'check': 'Domain Length',
                'status': 'warning',
                'message': 'Unusually long domain name'
            })

        if any(char.isdigit() for char in domain.replace('.', '')):
            domain_digits = sum(c.isdigit() for c in domain)
            if domain_digits > 3:
                checks.append({
                    'check':
                    'Domain Characters',
                    'status':
                    'warning',
                    'message':
                    f'Domain contains many numbers ({domain_digits})'
                })

        suspicious_words = [
            'verify', 'account', 'login', 'secure', 'update', 'confirm',
            'banking'
        ]
        if any(word in domain or word in path for word in suspicious_words):
            checks.append({
                'check': 'Suspicious Keywords',
                'status': 'warning',
                'message': 'URL contains phishing-related keywords'
            })

        if '-' in domain:
            hyphen_count = domain.count('-')
            if hyphen_count > 2:
                checks.append({
                    'check':
                    'Domain Format',
                    'status':
                    'warning',
                    'message':
                    f'Multiple hyphens in domain ({hyphen_count})'
                })

    except Exception as e:
        checks.append({
            'check': 'URL Parsing',
            'status': 'danger',
            'message': f'Invalid URL format: {str(e)}'
        })

    return checks
