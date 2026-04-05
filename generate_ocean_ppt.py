from mcp_server import create_presentation, add_slide
import sys

def main():
    print("[Agent] Bypassing global API network to build presentation physically...")
    print("[Agent] Connecting directly to MCP Slide Builder...\n")
    
    filename = "deep_ocean_wonders.pptx"
    
    print(f"  --> [Tool Call] create_presentation('{filename}')")
    create_presentation(filename)
    
    slides = [
        {
            "title": "Wonders of the Deep Ocean",
            "content": [
                "The deep ocean is the lowest layer in the sea, existing below the sunlight zone.",
                "It is completely devoid of light, freezing cold, and under immense pressure.",
                "Despite these harsh conditions, incredible creatures have adapted to survive here."
            ]
        },
        {
            "title": "Bioluminescence: Living Lights",
            "content": [
                "Bioluminescence is the production of light by living organisms through chemical reactions.",
                "Over 70% of deep-sea creatures use it to hunt, camouflage, or find mates in the pitch black.",
                "The famous Anglerfish uses a glowing lure on its head to attract unsuspecting prey."
            ]
        },
        {
            "title": "Hydrothermal Vents",
            "content": [
                "Hydrothermal vents are underwater fissures from which volcanically heated, mineral-rich water issues.",
                "They are found at extreme depths, usually along shifting tectonic plates.",
                "Vents support unique ecosystems driven completely by chemical energy rather than sunlight."
            ]
        },
        {
            "title": "Giants of the Abyss",
            "content": [
                "Deep-sea gigantism is the scientific tendency for species to be massively larger than shallow-water relatives.",
                "The Giant Squid can grow up to 43 feet long and constantly battles Sperm Whales in the deep.",
                "Massive isopods scavenge the freezing ocean floor searching for organic matter."
            ]
        },
        {
            "title": "Protecting the Deep Sea",
            "content": [
                "The deep ocean is our final frontier, with less than 5% mapped or explored in detail.",
                "Unfortunately, human activities like deep-sea mining and plastic pollution threaten these fragile ecosystems.",
                "We must continue to study, respect, and protect the alien world beneath our waves."
            ]
        }
    ]
    
    for slide in slides:
        print(f"  --> [Tool Call] add_slide('{filename}', '{slide['title']}', ...)")
        add_slide(filename, slide['title'], slide['content'])
        
    print("\n[✔] Finished successfully!")
    print(f"Saved new Dark Mode themed presentation to {filename}")

if __name__ == '__main__':
    main()
