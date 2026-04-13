from bs4 import BeautifulSoup

def clean(tag):
    """Extract text from a tag, replacing <hr> separators with ' | '."""
    if tag is None:
        return ""
    for hr in tag.find_all("hr"):
        hr.replace_with(" | ")
    return tag.get_text(separator=" ", strip=True)


def parse_phone_spec(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    # Index all data-spec cells for direct lookup
    spec = {
        tag["data-spec"]: clean(tag)
        for tag in soup.find_all(attrs={"data-spec": True})
        if tag.get("data-spec")
    }

    # Helper to check Yes/No cells by label text
    def yes_no(label: str) -> bool:
        for td in soup.find_all("td", class_="ttl"):
            if label.lower() in td.get_text(strip=True).lower():
                nfo = td.find_next_sibling("td", class_="nfo")
                if nfo:
                    return nfo.get_text(strip=True).lower() == "yes"
        return False

    return {
        "image": _parse_image(soup),
        "title": soup.find("title").get_text(strip=True).split('-')[0],
        # Network
        "network_technology": spec.get("nettech", ""),
        "network_2g_bands":   spec.get("net2g", ""),
        "network_3g_bands":   spec.get("net3g", ""),
        "network_4g_bands":   spec.get("net4g", ""),
        "network_5g_bands":   spec.get("net5g", ""),
        "network_speed":      spec.get("speed", ""),

        # Launch
        "announced": spec.get("year", ""),
        "status":    spec.get("status", ""),

        # Body
        "dimensions": spec.get("dimensions", ""),
        "weight":     spec.get("weight", ""),
        "sim":        spec.get("sim", ""),
        "body_other": spec.get("bodyother", ""),

        # Display
        "display_type":       spec.get("displaytype", ""),
        "display_size":       spec.get("displaysize", ""),
        "display_resolution": spec.get("displayresolution", ""),
        "display_protection": spec.get("displayprotection", ""),

        # Platform
        "os":      spec.get("os", ""),
        "chipset": spec.get("chipset", ""),
        "cpu":     spec.get("cpu", ""),
        "gpu":     spec.get("gpu", ""),

        # Memory
        "card_slot":       spec.get("memoryslot", ""),
        "internal_memory": spec.get("internalmemory", ""),
        "memory_type":     spec.get("memoryother", ""),

        # Main Camera
        "main_camera_modules":  spec.get("cam1modules", ""),
        "main_camera_features": spec.get("cam1features", ""),
        "main_camera_video":    spec.get("cam1video", ""),

        # Selfie Camera
        "selfie_camera_modules": spec.get("cam2modules", ""),
        "selfie_camera_video":   spec.get("cam2video", ""),

        # Sound
        "loudspeaker":    yes_no("loudspeaker"),
        "headphone_jack": yes_no("3.5mm jack"),

        # Comms
        "wlan":           spec.get("wlan", ""),
        "bluetooth":      spec.get("bluetooth", ""),
        "positioning":    spec.get("gps", ""),
        "nfc":            spec.get("nfc", "").lower() == "yes",
        "infrared_port":  yes_no("infrared port"),
        "radio":          spec.get("radio", ""),
        "usb":            spec.get("usb", ""),

        # Features
        "sensors": spec.get("sensors", ""),

        # Battery
        "battery_type": spec.get("batdescription1", ""),
        "charging": _charging_text(soup),

        # Misc
        "colors": spec.get("colors", ""),
        "price":  spec.get("price", ""),

        # EU Label
        "eu_energy_class":       _eu_label(soup, "Energy"),
        "eu_battery_endurance":  _eu_label(soup, "Battery"),
        "eu_free_fall_class":    _eu_label(soup, "Free fall"),
        "eu_repairability_class": _eu_label(soup, "Repairability"),
    }


def _charging_text(soup) -> str:
    """Charging has no data-spec; find it by its sibling label."""
    for td in soup.find_all("td", class_="ttl"):
        if "charging" in td.get_text(strip=True).lower():
            nfo = td.find_next_sibling("td", class_="nfo")
            if nfo:
                for hr in nfo.find_all("hr"):
                    hr.replace_with(" | ")
                return nfo.get_text(separator=" ", strip=True)
    return ""

def _parse_image(soup) -> str:
    photo_div = soup.find("div", class_="specs-photo-main")
    if not photo_div:
        return ""    
    img = photo_div.find("img")
    if not img:
        return ""    
    return img.get("src", "")

def _eu_label(soup, label: str) -> str:
    for td in soup.find_all("td", class_="ttl"):
        if label.lower() == td.get_text(strip=True).lower():
            nfo = td.find_next_sibling("td", class_="nfo")
            if nfo:
                return nfo.get_text(strip=True)
    return ""


# ── Save to DB ────────────────────────────────────────────────────────────────

def save_phone_spec(html: str):
    """Parse HTML and create/update a PhoneSpec record."""
    return parse_phone_spec(html)
    
