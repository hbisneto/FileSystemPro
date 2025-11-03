# filesystem/device/tests/test_network.py

from filesystem import device
network = device.network

# ================================================================================
print("=" * 80)
print("[NETWORK INFORMATION]: Program 1")
print("=" * 80)
# ================================================================================
print(f"Wi-Fi recebido: {network.get_wifi_received_bytes() / 1024**2:.2f} MB")
print(f"IP Wi-Fi: {network.get_wifi_ip()}")
print(f"Velocidade Wi-Fi: {network.get_wifi_speed_mbps()} Mbps")
print(f"Ethernet enviado: {network.get_ethernet_sent_bytes() / 1024**2:.2f} MB")
print(f"Total ↓: {network.get_total_received_bytes() / 1024**3:.2f} GB")
for conn in network.get_active_tcp_connections():
    print(f"→ {conn['remote_ip']}:{conn['remote_port']} (PID: {conn['pid']})")
# ================================================================================

# ================================================================================
print("=" * 80)
print("[NETWORK INFORMATION]: Program 2")
print("=" * 80)
# ================================================================================
print(f"Wi-Fi: {network.get_wifi_ip()} | {network.get_wifi_speed_mbps()} Mbps")
print(f"Ethernet: {network.get_ethernet_received_bytes() / 1024**3:.2f} GB recebidos")
print(f"Drop Wi-Fi: {network.get_wifi_dropped_packets()} pacotes")
print(f"Interfaces: {list(network.get_all_interfaces().keys())}")
# ================================================================================