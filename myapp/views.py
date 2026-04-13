import time
from django.shortcuts import get_object_or_404, render
from django.conf import settings
from django.http import HttpResponse
from django.views import View
from .models import PhoneSpec, NoPhone
from .utils import save_phone_spec

TOTAL_PHONES = 14_591+1
def home(request):
    print(PhoneSpec.objects.count(),NoPhone.objects.count())
    print([n.number for n in NoPhone.objects.all()])
    q = request.GET.get("q", "").strip()
    qs = PhoneSpec.objects.none()
    if q:
        qs = PhoneSpec.objects.filter(title__icontains=q).order_by("number")
    return render(
        request,
        "home.html",
        {
            "q": q,
            "results": qs,
            "result_count": qs.count() if q else 0,
        },
    )

def download_images(request):
    import os,requests
    for i in range(1,TOTAL_PHONES):
        url = PhoneSpec.objects.filter(number=i).first()
        if not url:
            continue
        filename = os.path.join("scraped_pages","images", f"{i}.jpg")
        if os.path.exists(filename):
            # print(f"File exists:{i}")
            continue
        try:
            response = requests.get(url.image, stream=True)
        except Exception as e:
            print(f'Request error at number {i}:{e}')
            continue
        
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print("Downloaded:", filename)
        else:
            print(f"Failed to download:{i}")
            continue
    return HttpResponse('completed')

def parse(request):
    start = time.perf_counter()
    NoPhone.objects.all().delete()
    FD = settings.BASE_DIR / 'scraped_pages'
    phonespec_list = []
    nophone_list = []

    existing_numbers = set(PhoneSpec.objects.values_list("number", flat=True))
    existing_numbers.update(NoPhone.objects.values_list("number", flat=True))

    for i in range(1, TOTAL_PHONES):
        if i in existing_numbers:
            continue
        path = FD / f"{i}.html"
        if not path.exists():
            nophone_list.append(NoPhone(number=i, error="File not found"))
            continue
        try:
            html = path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            nophone_list.append(NoPhone(number=i,error=str(e)))
            continue
        try:
            data = save_phone_spec(html)
        except Exception as e:
            nophone_list.append(NoPhone(number=i,error=str(e)))
            continue
        phonespec_list.append(PhoneSpec(number=i, **data,))
        if i%500==0:
            print('going to bulk create at ',i)
            NoPhone.objects.bulk_create(nophone_list)
            PhoneSpec.objects.bulk_create(phonespec_list)
            phonespec_list.clear()
            nophone_list.clear()          
            print('-')
    NoPhone.objects.bulk_create(nophone_list)
    PhoneSpec.objects.bulk_create(phonespec_list)
    return HttpResponse(f"Time taken: {time.perf_counter() - start:.6f} seconds")


class PhoneDetail(View):
    def _row(self,label, value, *, kind="text", linebreaks=False, always=False):
        if kind == "bool":
            return {
                "label": label,
                "value": bool(value),
                "kind": "bool",
            }
        if value is None or value == "":
            return None if not always else {
                "label": label,
                "value": "",
                "kind": "text",
                "linebreaks": linebreaks,
            }
        return {
            "label": label,
            "value": value,
            "kind": kind,
            "linebreaks": linebreaks,
        }

    def build_spec_sections(self,phone):
        sections = [
            {
                "title": "NETWORK",
                "rows": [
                    self._row("Technology", phone.network_technology),
                    self._row("2G Bands", phone.network_2g_bands),
                    self._row("3G Bands", phone.network_3g_bands),
                    self._row("4G Bands", phone.network_4g_bands),
                    self._row("5G Bands", phone.network_5g_bands),
                    self._row("Speed", phone.network_speed),
                ],
            },
            {
                "title": "LAUNCH",
                "rows": [
                    self._row("Announced", phone.announced),
                    self._row("Status", phone.status),
                ],
            },
            {
                "title": "BODY",
                "rows": [
                    self._row("Dimensions", phone.dimensions),
                    self._row("Weight", phone.weight),
                    self._row("SIM", phone.sim),
                    self._row("Other", phone.body_other),
                ],
            },
            {
                "title": "DISPLAY",
                "rows": [
                    self._row("Type", phone.display_type),
                    self._row("Size", phone.display_size),
                    self._row("Resolution", phone.display_resolution),
                    self._row("Protection", phone.display_protection),
                ],
            },
            {
                "title": "PLATFORM",
                "rows": [
                    self._row("OS", phone.os),
                    self._row("Chipset", phone.chipset),
                    self._row("CPU", phone.cpu),
                    self._row("GPU", phone.gpu),
                ],
            },
            {
                "title": "MEMORY",
                "rows": [
                    self._row("Card Slot", phone.card_slot),
                    self._row("Internal", phone.internal_memory),
                    self._row("Type", phone.memory_type),
                ],
            },
            {
                "title": "MAIN CAMERA",
                "rows": [
                    self._row("Modules", phone.main_camera_modules, linebreaks=True),
                    self._row("Features", phone.main_camera_features),
                    self._row("Video", phone.main_camera_video),
                ],
            },
            {
                "title": "SELFIE CAMERA",
                "rows": [
                    self._row("Modules", phone.selfie_camera_modules),
                    self._row("Video", phone.selfie_camera_video),
                ],
            },
            {
                "title": "SOUND",
                "rows": [
                    self._row("Loudspeaker", phone.loudspeaker, kind="bool"),
                    self._row("3.5mm Jack", phone.headphone_jack, kind="bool"),
                ],
            },
            {
                "title": "COMMS",
                "rows": [
                    self._row("WLAN", phone.wlan),
                    self._row("Bluetooth", phone.bluetooth),
                    self._row("Positioning", phone.positioning),
                    self._row("NFC", phone.nfc, kind="bool"),
                    self._row("Infrared", phone.infrared_port, kind="bool"),
                    self._row("Radio", phone.radio),
                    self._row("USB", phone.usb),
                ],
            },
            {
                "title": "FEATURES",
                "rows": [
                    self._row("Sensors", phone.sensors),
                ],
            },
            {
                "title": "BATTERY",
                "rows": [
                    self._row("Type", phone.battery_type),
                    self._row("Charging", phone.charging, linebreaks=True),
                ],
            },
            {
                "title": "MISC",
                "rows": [
                    self._row("Colors", phone.colors),
                    self._row("Price", phone.price),
                ],
            },
            {
                "title": "EU LABEL",
                "rows": [
                    self._row("Energy Class", phone.eu_energy_class),
                    self._row("Battery Endurance", phone.eu_battery_endurance),
                    self._row("Free Fall Class", phone.eu_free_fall_class),
                    self._row("Repairability Class", phone.eu_repairability_class),
                ],
            },
        ]
        cleaned = []
        for section in sections:
            rows = [row for row in section["rows"] if row is not None]
            if rows:
                cleaned.append({"title": section["title"], "rows": rows})
        return cleaned

    def get(self, request,n):
        phone = get_object_or_404(PhoneSpec, number=n)
        sect = self.build_spec_sections(phone)
        return render(request,"phone.html",{"phone": phone,"spec_sections": sect})
        
