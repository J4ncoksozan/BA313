iimport socket
import sys
import ssl
import time
from urllib.parse import urlparse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor

# In-memory session tracking (RAM only, fully purged on exit)
SESSION_METRICS = {
    "total_packets": 0,
    "network_types": {"Local Loopback": 0, "Private LAN": 0, "Attacks 🚀☀️": 0, "Invalid/Unknown": 0},
    "http_status_distribution": {
        "200 OK": 0,
        "3xx Redirect": 0,
        "400 Bad Request": 0,
        "401/403 Unauthorized": 0,
        "404 Not Found": 0,
        "5xx Server Error": 0,
        "Connection Dropped/Timed Out": 0
    },
    "total_rtt_latency": 0.0,
    "successful_network_handshakes": 0
}

def clean_target(user_input):
    """Parses input strings securely into domains, IPs, paths, and default structural schemes."""
    if not user_input.startswith(('http://', 'https://')):
        user_input = 'http://' + user_input
    parsed = urlparse(user_input)
    host = parsed.hostname if parsed.hostname else "127.0.0.1"
    port = parsed.port if parsed.port else (443 if parsed.scheme == 'https' else 80)
    path = parsed.path if parsed.path else "/"
    return host, port, parsed.scheme, path

def analyze_network_type(ip_address):
    """Categorizes the target into standard network layers and routing profiles."""
    try:
        if ip_address == "127.0.0.1" or ip_address.startswith("169.254."):
            return "Local Loopback"

        # Evaluate standard Private LAN subnet segments securely
        octets = [int(o) for o in ip_address.split('.')]
        if (octets[0] == 10 or
            (octets[0] == 172 and 16 <= octets[1] <= 31) or
            (octets[0] == 192 and octets[1] == 168)):
            return "Private LAN"

        return "Attacks 🚀☀️"
    except Exception:
        return "Invalid/Unknown"

def categorize_http_status(status_code):
    """Sorts numeric server signals into categorical debugging buckets."""
    if status_code == "200":
        return "200 OK"
    elif status_code.startswith("3"):
        return "3xx Redirect"
    elif status_code == "400":
        return "400 Bad Request"
    elif status_code in ["401", "403"]:
        return "401/403 Unauthorized"
    elif status_code == "404":
        return "404 Not Found"
    elif status_code.startswith("5"):
        return "5xx Server Error"
    return "Connection Dropped/Timed Out"

def execute_network_probe(host, port, scheme, path, timeout, net_type):
    """Fires network frames, maps out RTT latencies, and updates volatile data caches."""
    start_time = time.time()
    SESSION_METRICS["total_packets"] += 1
    SESSION_METRICS["network_types"][net_type] += 1

    try:
        if scheme == "https":
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            with socket.create_connection((host, port), timeout=timeout) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
                    ssock.sendall(request.encode())
                    response = ssock.recv(1024).decode('utf-8', errors='ignore')
        else:
            with socket.create_connection((host, port), timeout=timeout) as sock:
                request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
                sock.sendall(request.encode())
                response = sock.recv(1024).decode('utf-8', errors='ignore')

        rtt_latency = time.time() - start_time
        SESSION_METRICS["total_rtt_latency"] += rtt_latency
        SESSION_METRICS["successful_network_handshakes"] += 1

        status_str = "Unknown"
        if "HTTP/" in response:
            try:
                status_str = response.split(" ")[1]
            except IndexError:
                pass

        category = categorize_http_status(status_str)
        SESSION_METRICS["http_status_distribution"][category] += 1

        # Cyberpunk live status markers
        status_emoji = "💠”
        if status_str == "200":
            status_emoji = "🟢"
        elif status_str.startswith("3"):
            status_emoji = "🟡"
        elif status_str.startswith("4") or status_str.startswith("5"):
            status_emoji = "🔴”

        print(f"{status_emoji} [NET_STREAM] Route: {net_type} | Status: {status_str} | Latency: {rtt_latency:.4f}s")

    except Exception:
        SESSION_METRICS["http_status_distribution"]["Connection Dropped/Timed Out"] += 1
        print(f"💀 [DROP_ALERT] Route: {net_type} | Frame Status: Dropped/Filtered Network Pipeline")

def print_banner():
    """Renders the custom BA313 box art banner frame layout cleanly."""
    print("======    ==          ===      =======  ==  ==      ===       ======     ==     ==   ==     ==")
    print("==   ==   ==         == ==     ==       == ==      == ==      ==   ==    == === ==     ==  ==")
    print("======    ==        =======    ==       ===       =======     =====      ==  =  ==       ==")
    print("==   ==   ==       ==     ==   ==       == ==    ==     ==    ==   ==    ==     ==       ==")
    print("======    ======  ==       ==  =======  ==  ==  ==       ==   ==    ==   ==     ==       ==")
    print(" >> BA313 MATRIX ENGAGED // PALESTINE PERSISTENCE ACTIVE\n")

def print_summary():
    """Prints neon-styled summary statistics metrics."""
    avg_latency = (SESSION_METRICS["total_rtt_latency"] / SESSION_METRICS["successful_network_handshakes"]) if SESSION_METRICS["successful_network_handshakes"] > 0 else 0.0

    print("\n" + "🪩 " + "=" * 61 + " 🪩")
    print("               🔗  LIVE NETWORK TERMINAL SUMMARY  🔗               ")
    print("=" * 65)
    print(f" 🔈  Total Probes Dispatched:  {SESSION_METRICS['total_packets']}")
    print(f" ⌛️ Average Pipeline Latency:  {avg_latency:.4f} seconds")

    print("\n[💠] NETWORK ROUTING DISTRIBUTION:")
    for network, count in SESSION_METRICS["network_types"].items():
        if count > 0:
            print(f"  ⚡️ {network} Channels Active: {count} beams")

    print("\n[🎯] TARGET PROTOCOL DISTRIBUTION:")
    for status, count in SESSION_METRICS["http_status_distribution"].items():
        if count > 0:
            marker = "📟" if "200" in status else ("⚠️" if "400" in status or "Dropped" in status else "🔴")
            print(f"  {marker} {status}: {count} responses")

    print("=" * 65)
    print("✨️ [VOLATILE PURGE] Memory registers wiped cleanly. Session matrices dissolved.")

def main():
    print_banner()

    raw_target = input("🪩 Enter Target Core Link (URL/IP): ").strip()
    if not raw_target:
        print("❌️ [CRITICAL ERROR] Target input stream is blank.")
        return

    host, port, scheme, path = clean_target(raw_target)

    try:
        target_ip = socket.gethostbyname(host)
        net_type = analyze_network_type(target_ip)
    except socket.gaierror:
        print("❌️ [NET_FAILURE] Host resolution failed. Target isolated or offline.")
        return

    # User Configuration Input Engine
    print("\n🛠 [CONFIG ENGINE] Adjust parameters or press ENTER for Infinity parameters:")

    packet_input = input(" ■ Packets to stream [Default: ♾️]: ").strip()
    infinite_packets = False if packet_input else True
    total_packets = int(packet_input) if not infinite_packets else 0

    thread_input = input(" ■ Concurrent thread pipes [Default: Max OS Threading]: ").strip()
    threads = int(thread_input) if thread_input else None

    timeout_input = input(" ■ Timeout limit (Seconds) [Default: ♾️/None]: ").strip()
    timeout = float(timeout_input) if timeout_input else None

    print("\n🔈 " + "-" * 61 + " 🔈")
    print(f" 🪩 Target Endpoint:   {scheme}://{host}:{port}{path} ({target_ip})")
    print(f" 🀄 Network Layer:    {net_type}")
    print(f" ⚡️ Pipeline Load:    {'Infinity' if infinite_packets else total_packets} frames | {'Max Capacity' if threads is None else threads} workers")
    print(f" ⌛️ Expiry Vector:    {'Disabled (Infinite Hold)' if timeout is None else f'{timeout}s'}")
    print("-" * 65 + "\n")

    # Multithreading Execution Matrix
    try:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            if infinite_packets:
                print("☀️ [ATTACK ENGAGED] Continuous transmission online. Strike [Ctrl+C] to compile final data telemetry...\n")
                while True:
                    executor.submit(execute_network_probe, host, port, scheme, path, timeout, net_type)
                    time.sleep(0.001)  # Mitigates processor starvation
            else:
                print("☀️ [ATTACK ENGAGED] Finite transmission online.\n")
                futures = [executor.submit(execute_network_probe, host, port, scheme, path, timeout, net_type) for _ in range(total_packets)]
                for future in futures:
                    future.result()
    except KeyboardInterrupt:
        pass

    print_summary()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n☀️ [FORCED ABORT] Hard break intercepted. System RAM caches dropped immediately.")
        sys.exit()
