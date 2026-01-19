import random

POSES = [
    "Tadasana (Mountain Pose)", "Uttanasana (Forward Fold)", "Adho Mukha Svanasana (Downward Dog)",
    "Bhujangasana (Cobra Pose)", "Urdhva Mukha Svanasana (Upward Dog)", "Virabhadrasana I (Warrior I)",
    "Virabhadrasana II (Warrior II)", "Virabhadrasana III (Warrior III)", "Trikonasana (Triangle Pose)",
    "Parsvakonasana (Side Angle Pose)", "Prasarita Padottanasana (Wide-Legged Forward Fold)",
    "Vrksasana (Tree Pose)", "Garudasana (Eagle Pose)", "Ardha Chandrasana (Half Moon Pose)",
    "Utthita Trikonasana (Extended Triangle)", "Parivrtta Trikonasana (Revolved Triangle)",
    "Malasana (Garland Pose)", "Bhairavasana (Fierce Pose)", "Eka Pada Rajakapotasana (Pigeon Pose)",
    "Gomukhasana (Cow Face Pose)", "Baddha Konasana (Bound Angle Pose)", "Janu Sirsasana (Head-to-Knee Pose)",
    "Paschimottanasana (Seated Forward Fold)", "Upavistha Konasana (Wide-Angle Seated Forward Bend)",
    "Navasana (Boat Pose)", "Ardha Navasana (Half Boat Pose)", "Sarvangasana (Shoulder Stand)",
    "Halasana (Plow Pose)", "Matsyasana (Fish Pose)", "Bhakasana (Crow Pose)",
    "Adho Mukha Vrksasana (Downward-Facing Tree Pose)", "Scorpion Pose", "Handstand",
    "Headstand (Sirsasana)", "Shoulderstand (Sarvangasana)", "Bridge Pose (Setu Bandha Sarvangasana)",
    "Wheel Pose (Urdhva Mukha Paschimottanasana)", "Bow Pose (Dhanurasana)", "Locust Pose (Salabhasana)",
    "Child's Pose (Balasana)", "Corpse Pose (Savasana)", "Sitting Forward Bend", "Cat Pose (Marjaryasana)",
    "Cow Pose (Bitilasana)", "Happy Baby Pose", "Legs Up the Wall (Viparita Karani)"
]

BENEFITS = [
    "increases flexibility and range of motion", "strengthens core muscles",
    "improves balance and proprioception", "enhances cardiovascular health",
    "reduces stress and anxiety", "promotes relaxation and better sleep",
    "improves digestion and metabolism", "boosts immune system",
    "increases energy and vitality", "improves mental clarity and focus",
    "reduces chronic pain", "enhances spinal health",
    "improves hip opening and mobility", "strengthens leg muscles",
    "opens the chest and improves breathing", "calms the nervous system",
    "improves posture and alignment", "reduces tension in shoulders and neck",
    "enhances body awareness", "improves concentration",
    "promotes inner peace", "builds strength and endurance",
    "increases blood circulation", "improves joint health",
    "reduces lower back pain", "strengthens the spine",
    "improves hamstring flexibility", "opens the hip flexors",
    "enhances shoulder stability", "improves wrist strength",
    "increases spinal mobility", "promotes detoxification"
]

CONTRAINDICATIONS = [
    "avoid if you have shoulder pain or injury", "not recommended during pregnancy",
    "skip if you have high blood pressure", "avoid if you have wrist issues",
    "contraindicated for lower back injuries", "skip if you have neck problems",
    "avoid if you have herniated discs", "not suitable for knee injuries",
    "avoid if you have glaucoma or eye problems", "skip if you have headaches or migraines",
    "contraindicated for hip injuries", "avoid if you have shoulder impingement",
    "not recommended for ankle sprains", "skip if you have hamstring injuries",
    "avoid if you recently ate a heavy meal", "not suitable for heart conditions",
    "avoid during menstruation (for some practitioners)", "skip if you have sciatica",
    "contraindicated for sacroiliac joint dysfunction", "avoid if you have carpal tunnel",
    "not recommended for rotator cuff injuries", "skip if you have shin splints",
    "avoid if you have plantar fasciitis", "not suitable for severe osteoporosis",
    "contraindicated for spinal stenosis", "avoid if you have dizziness",
    "skip if you have balance issues", "not recommended with uncontrolled diabetes",
    "avoid if you have recent abdominal surgery", "not suitable for severe arthritis",
    "contraindicated for detached retina", "avoid if you have anxiety disorders"
]

TECHNIQUES = [
    "hold for 30 seconds to 1 minute", "hold for 1-2 minutes for deeper practice",
    "focus on your breath throughout", "engage your core for stability",
    "ensure your spine remains neutral", "press firmly through your hands",
    "relax your shoulders away from ears", "keep your chest open",
    "distribute weight evenly", "breathe steadily and deeply",
    "avoid forcing the pose", "listen to your body's signals",
    "modifications available for beginners", "advanced variations for experienced yogis",
    "pair with complementary poses", "transition slowly and mindfully",
    "practice 3-5 times weekly for benefits", "warm up before attempting",
    "cool down and stretch afterward", "maintain alignment throughout",
    "engage your bandhas for energy control", "use props if needed (blocks, straps, blankets)"
]

CHAKRAS = [
    "grounds root chakra energy", "activates sacral chakra", 
    "strengthens solar plexus chakra", "opens heart chakra",
    "balances throat chakra", "activates third eye chakra",
    "connects to crown chakra", "aligns all seven chakras"
]

LEVELS = ["Beginner", "Intermediate", "Advanced", "Beginner-Intermediate", "Intermediate-Advanced"]


def generate_yoga_data(num_entries=1000):
    data_lines = []
    
    for i in range(num_entries):
        pose = random.choice(POSES)
        benefits = ", ".join(random.sample(BENEFITS, random.randint(2, 4)))
        contraindications = ", ".join(random.sample(CONTRAINDICATIONS, random.randint(1, 3)))
        technique = random.choice(TECHNIQUES)
        chakra = random.choice(CHAKRAS)
        level = random.choice(LEVELS)
        
        entry = f"""
YOGA POSE #{i+1}: {pose}
Difficulty Level: {level}
Primary Benefits: {benefits}
Precautions & Contraindications: {contraindications}
Technique Tips: {technique}
Chakra Association: {chakra}
---"""
        data_lines.append(entry)
    
    return "\n".join(data_lines)


def save_yoga_data(filename="yoga_data.txt"):
    print(f"Generating {1000} yoga data entries...")
    data = generate_yoga_data(1000)
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(data)
    
    print(f"Successfully saved {len(data.split('---'))} yoga entries to {filename}")
    print(f"File size: {len(data) / 1024:.2f} KB")


if __name__ == "__main__":
    save_yoga_data("yoga_data.txt")
