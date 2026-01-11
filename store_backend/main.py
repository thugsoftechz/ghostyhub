from fastapi import FastAPI, HTTPException, Query
from typing import List
from models import PackageManifest, PackageType, SearchResult

app = FastAPI(title="GhostyHub App Store API", version="1.0")

# Mock Database
MOCK_DB: List[PackageManifest] = [
    PackageManifest(
        id="com.indiegame.pixelracer",
        name="Pixel Racer",
        version="1.2.0",
        type=PackageType.GAME,
        description="A high-speed retro racing game.",
        runtime="proton",
        permissions=["gpu", "controller", "network"],
        signature="ED25519:ABCD1234",
        price_usd=0.0,
        developer="IndieDev Studios",
        download_url="https://cdn.ghostyhub.io/packages/pixelracer.ghpkg"
    ),
    PackageManifest(
        id="org.libretro.retroarch",
        name="RetroArch",
        version="1.16.0",
        type=PackageType.EMULATOR,
        description="Frontend for emulators, game engines and media players.",
        permissions=["gpu", "controller", "storage"],
        signature="ED25519:BCDE5678",
        price_usd=0.0,
        developer="Libretro Team",
        download_url="https://cdn.ghostyhub.io/packages/retroarch.ghpkg"
    ),
    PackageManifest(
        id="com.ghostyhub.ai.pro",
        name="GhostyHub AI Pro Tuning",
        version="2.0.0",
        type=PackageType.TOOL,
        description="Advanced AI models for specific AAA titles.",
        permissions=["root", "ai_engine"],
        signature="ED25519:CDEF9012",
        price_usd=15.0,
        developer="GhostyHub Core",
        download_url="https://cdn.ghostyhub.io/packages/ai_pro.ghpkg"
    )
]

@app.get("/")
def read_root():
    return {"message": "Welcome to GhostyHub App Store API"}

@app.get("/packages", response_model=SearchResult)
def search_packages(
    q: str = Query(None, min_length=3),
    category: PackageType = None
):
    results = MOCK_DB

    if category:
        results = [p for p in results if p.type == category]

    if q:
        q = q.lower()
        results = [p for p in results if q in p.name.lower() or q in p.description.lower()]

    return SearchResult(packages=results, total=len(results))

@app.get("/packages/{package_id}", response_model=PackageManifest)
def get_package(package_id: str):
    for p in MOCK_DB:
        if p.id == package_id:
            return p
    raise HTTPException(status_code=404, detail="Package not found")

@app.post("/install/{package_id}")
def install_package(package_id: str):
    # In a real scenario, this would generate a signed download link or transaction
    for p in MOCK_DB:
        if p.id == package_id:
            return {"status": "downloading", "url": p.download_url, "signature": p.signature}
    raise HTTPException(status_code=404, detail="Package not found")
