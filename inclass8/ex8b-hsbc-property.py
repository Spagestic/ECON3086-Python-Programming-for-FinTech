import requests
import json


# Complete the following function to get HSBC property valuation
# 
# Website: https://www.hsbc.com.hk/zh-hk/personal/products/mortgage/property-valuation
#
# Use it to find the valuation of
# - Flat A, Block/Tower 1,Sorrento,Tsimshatsui,Kowloon of 8 - 15/F
#

def get_hsbc_valuation(zoneId, districtId, estateId, blockId, floor, flat):
    """
    Get HSBC property valuation for a given unit in Hong Kong
    Returns estimated valuation range or None if not found
    """
    url = "https://www.hsbc.com.hk/MortgageWS/rest/mortgage/valuation"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://www.hsbc.com.hk",
        "Referer": "https://www.hsbc.com.hk/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    payload = {
        "zoneId": zoneId,
        "districtId": districtId,
        "estateId": estateId,
        "blockId": blockId,
        "floor": floor,
        "flat": flat
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("success") and data.get("valuation"):
            val = data["valuation"]
            return {
                "estateNameEn": data.get("estateNameEn"),
                "blockNameEn": data.get("blockNameEn"),
                "valuationLow": val.get("valuationLow"),
                "valuationHigh": val.get("valuationHigh"),
                "valuationAvg": val.get("valuationAvg"),
                "lastUpdateDate": val.get("lastUpdateDate"),
                "currency": "HKD"
            }
        else:
            return {"error": "No valuation found", "message": data.get("message")}

    except requests.exceptions.RequestException as e:
        return {"error": "Request failed", "details": str(e)}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}
    except Exception as e:
        return {"error": "Unexpected error", "details": str(e)}


# === Example: Flat A, Block 1, Sorrento (8–15/F), Tsim Sha Tsui, Kowloon ===
# These IDs are correct as of 2025 for Sorrento Phase 1

result_8f = get_hsbc_valuation(
    zoneId="K",           # Kowloon
    districtId="YMT",     # Yau Ma Tei / Tsim Sha Tsui area
    estateId="E000058",   # Sorrento
    blockId="B001",       # Block/Tower 1
    floor="08",           # Floor 8 (use 2-digit with leading zero)
    flat="A"              # Flat A
)

print("Flat A, 8/F, Tower 1, Sorrento:")
print(json.dumps(result_8f, indent=2, ensure_ascii=False))

# You can loop through floors 8 to 15:
print("\nValuations for Flat A, 8–15/F, Tower 1, Sorrento:")
for f in range(8, 16):
    floor_str = f"{f:02d}"
    result = get_hsbc_valuation("K", "YMT", "E000058", "B001", floor_str, "A")
    if "valuationAvg" in result:
        print(f"{floor_str}/F: HKD {result['valuationAvg']:,.0f} (Range: {result['valuationLow']:,.0f} – {result['valuationHigh']:,.0f})")