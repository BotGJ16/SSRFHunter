## **🚀 SSRFHunter Elite v3.0 - Command Reference for Bug Bounty**

### **📦 Installation Commands**

```bash
# 1. Install Go tools (pehli baar)
go install github.com/lc/gau/v2/cmd/gau@latest
go install github.com/projectdiscovery/katana/cmd/katana@latest
go install github.com/tomnomnom/waybackurls@latest
go install github.com/projectdiscovery/urlfinder/cmd/urlfinder@latest

# 2. Verify installation
which gau katana waybackurls urlfinder

# 3. Install Python dependencies
pip install aiohttp aiofiles websocket-client

# 4. Download tool
git clone https://github.com/BotGJ16/GF_Patterns/
cd GF_Patterns
chmod +x ssrfhunter_elite_v3.py
```

***

### **🎯 Basic Bug Bounty Commands**

#### **Command 1: Single Domain (Quick Recon)**
```bash
python ssrfhunter_elite_v3.py -d target.com -o results/target.com/
```
**Use Case**: Pehli baar target scan karna, jaldi se SSRF check karna
**Output**: `results/target.com/ssrf_report_2025.md`

#### **Command 2: Wildcard Domain (Full Scope)**
```bash
python ssrfhunter_elite_v3.py -d "*.target.com" -o results/target-all/ --concurrency 20
```
**Use Case**: Jab program mein `*.target.com` scope ho, sab subdomains scan karna
**Pro Tip**: `--concurrency 20` se 20 parallel requests, time bachta hai

#### **Command 3: Stealth Mode (Live Target)**
```bash
python ssrfhunter_elite_v3.py -d api.target.com -o results/api-stealth/ --stealth --concurrency 5
```
**Use Case**: Production target jahan rate-limiting ya WAF ho, undetectable rehna
**Feature**: Har request ke beech 1-5 second random delay

***

### **🔐 Authenticated Testing Commands**

#### **Command 4: Cookie-Based Authentication**
```bash
python ssrfhunter_elite_v3.py -d app.target.com -o results/auth/ \
  --session user1 \
  --cookie "session=abc123;auth_token=xyz789"
```
**Use Case**: Jab login ke baad SSRF ho, authenticated endpoints test karna
**Exploit**: Admin panels mein SSRF, internal admin tools access

#### **Command 5: JWT Token Authentication**
```bash
python ssrfhunter_elite_v3.py -d api.target.com -o results/jwt/ \
  --session admin \
  --jwt "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
```
**Use Case**: JWT-protected APIs, GraphQL endpoints, serverless functions
**Impact**: JWT validation ke baad internal services access

#### **Command 6: Custom Headers + Cookies**
```bash
python ssrfhunter_elite_v3.py -d internal.target.com -o results/custom-auth/ \
  --session dev \
  --cookie "PHPSESSID=abc;csrf=xyz" \
  --header "X-API-Key:secret123,Authorization:Bearer token456"
```
**Use Case**: Complex authentication (API keys, CSRF tokens, custom headers)
**Finding**: Internal dev tools, staging environments

***

### **🎭 Stealth & OPSEC Commands**

#### **Command 7: Through Burp Proxy (Manual Analysis)**
```bash
python ssrfhunter_elite_v3.py -d target.com -o results/burp/ \
  --proxy http://127.0.0.1:8080 \
  --stealth \
  --concurrency 3
```
**Use Case**: Har request ko Burp mein dekhna, manual tampering karna
**Pro Tip**: Burp ke "Target" tab mein scope set karo, saste mein sara traffic capture ho jayega

#### **Command 8: SOCKS5 Proxy (IP Rotation)**
```bash
python ssrfhunter_elite_v3.py -d target.com -o results/socks/ \
  --proxy socks5://127.0.0.1:9050 \
  --stealth
```
**Use Case**: IP rotate karna, rate-limit bypass karna, anonymous rehna
**Setup**: Tor ya SOCKS5 proxy chahiye (e.g., `proxychains`)

#### **Command 9: Ultra-Stealth (Critical Target)**
```bash
python ssrfhunter_elite_v3.py -d banking.target.com -o results/stealth/ \
  --stealth \
  --concurrency 1 \
  --proxy http://burp:8080
```
**Use Case**: Banking, fintech jahan detection = banned
**Feature**: Har request ke baad 1-5 second random delay + single request

***

### **☁️ Cloud & Platform-Specific Commands**

#### **Command 10: AWS Target (IMDSv2 Bypass)**
```bash
python ssrfhunter_elite_v3.py -d ec2-app.target.com -o results/aws/ --ai-platform
```
**Use Case**: AWS-hosted apps, check IMDSv2 bypass
**Finding**: `http://169.254.169.254/latest/api/token` access
**Impact**: IAM role credentials leak → full AWS account takeover

#### **Command 11: Azure AI Platform (CVE-2025-53767)**
```bash
python ssrfhunter_elite_v3.py -d openai.azure.com -o results/azure-ai/ --ai-platform --jwt "$AAD_TOKEN"
```
**Use Case**: Azure OpenAI endpoints, AI service exploitation
**CVE**: CVE-2025-53767 (Azure AI SSRF to internal management)
**Impact**: AI model theft, billing abuse, internal network access

#### **Command 12: GCP Functions**
```bash
python ssrfhunter_elite_v3.py -d gcp-functions.target.com -o results/gcp/ --ai-platform
```
**Use Case**: GCP Cloud Functions, serverless metadata abuse
**Finding**: `http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token`

***

### **🐳 Kubernetes & Container Commands**

#### **Command 13: K8s Internal Scan**
```bash
python ssrfhunter_elite_v3.py -d k8s-dashboard.target.com -o results/k8s/ --internal-scan --container-escape
```
**Use Case**: Kubernetes dashboard, internal services
**Impact**: K8s API access → pod exec → host escape

#### **Command 14: Container Escape Testing**
```bash
python ssrfhunter_elite_v3.py -d docker-app.target.com -o results/docker/ --container-escape --full-arsenal
```
**Use Case**: Docker socket expose hua ho, container breakout test karna
**CVE**: CVE-2025-31133 (runc container escape)
**Exploit**: `http://127.0.0.1:2375/containers/json`

***

### **📊 GraphQL & WebSocket Commands**

#### **Command 15: GraphQL Endpoint SSRF**
```bash
python ssrfhunter_elite_v3.py -d api.target.com -o results/graphql/ --jwt "$JWT"
```
**Auto-Detect**: `/graphql`, `/gql`, `/query` endpoints
**Test**: Field resolvers mein SSRF (e.g., `user(avatarUrl: "URL")`)
**Finding**: GraphQL nested query SSRF

#### **Command 16: WebSocket SSRF**
```bash
python ssrfhunter_elite_v3.py -d realtime.target.com -o results/websocket/ --full-arsenal
```
**Auto-Detect**: `ws://`, `wss://` endpoints
**Test**: WebSocket handshake SSRF
**Impact**: Real-time data exfiltration, internal service access

***

### **🔄 Bulk & Automation Commands**

#### **Command 17: Bulk Domain Scan (from file)**
```bash
# domains.txt mein line-by-line domains
cat domains.txt | while read domain; do
  python ssrfhunter_elite_v3.py -d "$domain" -o "results/bulk/$domain/" --concurrency 10
done
```
**Use Case**: Multiple targets, bug bounty program ka pura scope
**Output**: Har domain ke liye alag folder

#### **Command 18: Parallel Bulk Scan (GNU Parallel)**
```bash
# 5 parallel scans
cat domains.txt | parallel -j5 python ssrfhunter_elite_v3.py -d {} -o results/parallel/{}
```
**Use Case**: Time bachana, 100+ domains quickly scan karna
**Requirement**: `apt install parallel` ya `brew install parallel`

#### **Command 19: CI/CD Integration**
```bash
# Jenkins/GitLab pipeline
python ssrfhunter_elite_v3.py -d "$TARGET" -o results/ --json-output
if grep -q '"confidence":"critical"' results/ssrf_results_2025.json; then
  echo "CRITICAL SSRF found!"
  exit 1
fi
```
**Use Case**: Automated security scanning, pipeline fail on critical

***

### **🎨 Report Generation Commands**

#### **Command 20: Generate Report Only**
```bash
# Agar pehle se results.json hai, sirf report generate karo
python -c "
import json
data = json.load(open('results/ssrf_results_2025.json'))
# Report generation logic yahan
"
```
**Use Case**: Results ko alag format mein convert karna

#### **Command 21: Extract High-Confidence Findings**
```bash
# Sirf critical aur high confidence findings nikalo
cat results/ssrf_results_2025.json | jq '.[] | select(.confidence=="critical" or .confidence=="high")'
```
**Use Case**: Bug report mein sirf best findings daalna
**Tool**: `apt install jq` (JSON parser)

#### **Command 22: Cloud Credentials Extract**
```bash
# Sab credentials ek file mein nikalo
cat results/ssrf_results_2025.json | jq -r '.[] | select(.metadata_leaked==true) | .credentials_found[] | .value'
```
**Use Case**: Cloud security audit, leaked keys check karna

***

### **🔥 Pro Bug Bounty Commands**

#### **Command 23: P1 Priority Scan (Critical Only)**
```bash
# Sirf high-impact targets (admin, internal, cloud)
python ssrfhunter_elite_v3.py -d admin.target.com -o results/p1/ --full-arsenal --concurrency 15
```
**Strategy**: Admin panels, internal tools, cloud consoles pehle scan karo
**Impact**: Milte hi $$$$ bounty

#### **Command 24: Stealth + Evidence Recording**
```bash
# Scan karte time Burp mein har request capture karo
python ssrfhunter_elite_v3.py -d target.com -o results/evidence/ \
  --proxy http://127.0.0.1:8080 \
  --stealth \
  --concurrency 3

# Burp mein right-click → Save item → POC ke liye use karo
```
**Use Case**: Report mein proof-of-concept video ke saath Burp requests attach karna

#### **Command 25: Serverless Functions Targeting**
```bash
# Lambda, GCP Functions, Azure Functions
python ssrfhunter_elite_v3.py -d "*.execute-api.target.com" -o results/serverless/ --ai-platform --full-arsenal
```
**Finding**: `AWS_LAMBDA_RUNTIME_API` access, function metadata leak
**Impact**: Serverless RCE, billing fraud, lateral movement

***

### **📱 Mobile API Commands**

#### **Command 26: Mobile App Backend (API)**
```bash
python ssrfhunter_elite_v3.py -d api.mobile.target.com -o results/mobile/ \
  --header "User-Agent:MobileApp/2.0.1,Authorization:Bearer $MOBILE_TOKEN" \
  --stealth
```
**Use Case**: Mobile app ke backend API scan karna
**Finding**: Mobile-specific endpoints mein SSRF

***

### **🌐 Multi-Target Automation**

#### **Command 27: Subfinder + SSRFHunter Chain**
```bash
# Pehle subdomains nikalo, phir SSRF scan karo
subfinder -d target.com -silent | while read subdomain; do
  python ssrfhunter_elite_v3.py -d "$subdomain" -o "results/subfinder/$subdomain/" --concurrency 5
done
```
**Use Case**: Complete subdomain enumeration + SSRF testing
**Tools**: Subfinder, then SSRFHunter

#### **Command 28: Asset Discovery + SSRF**
```bash
# Amass + SSRFHunter workflow
amass enum -d target.com -passive | tee domains.txt
cat domains.txt | parallel -j3 python ssrfhunter_elite_v3.py -d {} -o results/amass/{}
```
**Use Case**: Asset discovery ke baad SSRF testing
**Tools**: Amass, then parallel SSRFHunter

***

### **🎁 Bonus: Quick Reference Card**

| Scenario | Command | Expected Finding |
|----------|---------|------------------|
| Quick test | `-d target.com -o results/` | Basic SSRF |
| Wildcard scan | `-d "*.target.com" -o results/ --concurrency 20` | Subdomain SSRF |
| Stealth scan | `--stealth --concurrency 3` | Avoid WAF/rate-limit |
| Auth scan | `--session admin --cookie "sess=abc"` | Internal SSRF |
| Cloud target | `--ai-platform` | AWS/GCP/Azure metadata |
| K8s target | `--internal-scan --container-escape` | Container escape |
| GraphQL | `-d api.target.com --jwt "$JWT"` | GraphQL resolver SSRF |
| WebSocket | `-d realtime.target.com` | ws:// SSRF |
| Bulk scan | `cat domains.txt \| parallel ...` | 100+ domains |
| Evidence | `--proxy http://burp:8080` | Burp POC capture |

***

### **💡 Pro Tips for Bug Bounty**

1. **Pehle Stealth Mode**: Har target pe `--stealth` use karo, ban hone se bacho
2. **Authentication Zaroori**: Login ke baad ke endpoints pe zyada impact hota hai
3. **Cloud = $$$$**: `--ai-platform` se cloud metadata nikalo, highest bounty
4. **Report Ready**: `--proxy` se Burp capture karo, report mein attach karo
5. **Parallel = Time Bachao**: Bulk scan mein `parallel` use karo
6. **Evidence Pack**: `results/` folder ko zip karo, report ke saath submit karo

***
