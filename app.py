import os
import re
from datetime import datetime
from dotenv import load_dotenv
import streamlit as st
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint


load_dotenv()

HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN", "")
CHROMA_DB_PATH = "./chroma_db"

SAFETY_BLOCKED_KEYWORDS = ["kill", "hurt", "harm", "weapon", "violence", "attack", "injure"]

YOGA_KEYWORDS = [
    "yoga", "pose", "asana", "pranayama", "meditation", "chakra",
    "downward dog", "warrior", "lotus", "stretch", "flexibility",
    "breathing", "mudra", "mantra", "namaste", "hatha", "vinyasa",
    "yin yoga", "power yoga", "kundalini", "yogi", "asanas",
    "alignment", "chakras", "benefits", "technique", "posture",
    "flexibility", "strength", "balance", "relaxation", "stress relief",
    "pigeon", "child pose", "corpse pose", "mountain pose", "tree pose",
    "forward fold", "backbend", "hip opener", "sun salutation",
    "drishti", "ujjayi", "padmasana", "trikonasana", "cobra", "bhujang"
]


def check_safety(query: str) -> tuple[bool, str]:
    query_lower = query.lower()
    
    for keyword in SAFETY_BLOCKED_KEYWORDS:
        if keyword in query_lower:
            return False, f"Blocked keyword: {keyword}"
    
    harmful_words = ["suicide", "death", "kill"]
    if any(word in query_lower for word in harmful_words):
        return False, "Query contains potentially harmful content"
    
    return True, "Safe"


def is_yoga_question(query: str) -> bool:
    query_lower = query.lower()
    
    if any(keyword in query_lower for keyword in YOGA_KEYWORDS):
        return True
    
    general_yoga_words = ["how", "what", "why", "benefit", "help", "practice", "exercise", "health", "wellness", "fitness", "body", "mind"]
    if any(word in query_lower for word in general_yoga_words):
        return True
    
    return False


YOGA_KNOWLEDGE = """
YOGA FUNDAMENTALS

What is Yoga?
Yoga is an ancient practice from India that combines physical poses (asanas), breathing 
exercises (pranayama), and meditation to improve physical, mental, and spiritual health.

KEY BENEFITS OF YOGA:

Physical Benefits:
• Increased flexibility and range of motion
• Stronger muscles and bones
• Better balance and coordination
• Improved cardiovascular health
• Reduced chronic pain and stiffness

Mental & Emotional Benefits:
• Reduced stress and anxiety
• Better focus and concentration
• Improved sleep quality
• Greater emotional balance
• Increased self-awareness

Spiritual Benefits:
• Deeper mindfulness and awareness
• Inner peace and tranquility
• Connection to purpose
• Enhanced spiritual growth

POPULAR YOGA POSES:
• Mountain Pose (Tadasana) - foundation pose, improves posture
• Downward Dog (Adho Mukha Svanasana) - strengthens arms, calms mind
• Warrior I & II (Virabhadrasana) - build strength and confidence
• Child's Pose (Balasana) - promotes relaxation and calmness
• Tree Pose (Vrksasana) - improves balance and focus
• Lotus Pose (Padmasana) - opening pose for meditation
• Forward Fold (Uttanasana) - stretches hamstrings, calms mind

YOGA PRACTICE TIPS:
• Practice 3-5 times per week for best results
• Listen to your body - never force a pose
• Breathe deeply and steadily (never hold your breath)
• Warm up before attempting advanced poses
• Combine poses with meditation and breathing exercises
"""

@st.cache_resource
def load_yoga_data():
    if not os.path.exists("yoga_data.txt"):
        st.error("yoga_data.txt not found!")
        st.stop()
    
    with open("yoga_data.txt", "r", encoding="utf-8") as f:
        yoga_text = f.read()
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ".", " "]
    )
    return splitter.split_text(yoga_text)


@st.cache_resource
def create_vector_database(chunks):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={"device": "cpu"}
    )
    
    return Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB_PATH,
        collection_name="yoga_knowledge"
    )


@st.cache_resource
def setup_llm():
    if not HUGGINGFACE_API_TOKEN:
        return None
    
    try:
        return HuggingFaceEndpoint(
            repo_id="mistralai/Mistral-Large-Instruct-2411",
            huggingfacehub_api_token=HUGGINGFACE_API_TOKEN,
            max_new_tokens=1024,
            temperature=0.1,
            top_p=0.92,
            repetition_penalty=1.1
        )
    except:
        return None


def generate_fallback_response(query: str) -> str:
    query_lower = query.lower()
    
    if any(word in query_lower for word in ["benefit", "help", "good", "advantage"]):
        return """Amazing Benefits of Yoga:

Physical Benefits:
• Increased flexibility and strength
• Better balance and coordination
• Improved cardiovascular health
• Reduced chronic pain
• Better posture and alignment

Mental & Emotional:
• Reduced stress and anxiety
• Improved focus and concentration
• Better sleep quality
• Emotional stability and peace
• Increased self-awareness

Spiritual:
• Deeper mindfulness
• Inner peace and tranquility
• Connection to purpose
• Enhanced spiritual growth

Practice Regularly: 3-5 times per week for best results. Consistency beats intensity!"""
    
    elif any(word in query_lower for word in ["pose", "asana"]):
        if "downward dog" in query_lower:
            return """Downward Dog (Adho Mukha Svanasana)

What It Does:
• Strengthens arms, shoulders, legs
• Stretches hamstrings and calves
• Improves blood circulation
• Calms nervous system
• Reduces stress

How to Do It:
1. Start on hands and knees
2. Press palms firmly on ground
3. Lift hips toward ceiling
4. Create an inverted V-shape
5. Head between arms, breathe deeply
6. Hold 5-10 breaths

Beginner Tips:
• Bend your knees if needed
• Don't lock elbows
• Breathe deeply throughout

Avoid If: You have wrist/shoulder injuries"""
        else:
            return """Common Yoga Poses:

Standing: Mountain, Warrior I/II, Triangle - build strength
Forward Bends: Forward Fold, Seated Fold - stretch & calm
Backbends: Cobra, Wheel, Bridge - strengthen spine
Hip Openers: Pigeon, Butterfly - increase flexibility
Balance: Tree, Eagle - improve focus
Rest: Child's Pose, Corpse - relax & restore

Which pose interests you?"""
    
    elif any(word in query_lower for word in ["beginner", "start", "learn", "new"]):
        return """Your Yoga Journey Starts Here!

Week 1-2: Foundation
• Practice 2-3 times per week
• Learn: Mountain, Child's, Downward Dog
• Focus on breathing
• 20-30 minutes per session

Essential Beginner Poses:
• Mountain Pose - foundation
• Child's Pose - rest & calm
• Downward Dog - stretch & strengthen
• Forward Fold - flexibility
• Corpse Pose - final relaxation

Important Tips:
• Never force any pose
• Listen to your body
• Breathe deeply & steadily
• Rest between poses
• Wear comfortable clothes

What You'll Feel:
Week 2: Increased flexibility
Week 3: Strength improvement
Week 4+: Mental clarity & peace

Consistency is key - start now!"""
    
    else:
        return """Welcome to Your Yoga Assistant!

I'm here to help with:
• Yoga poses and how to do them
• Benefits and health improvements
• Breathing techniques
• Meditation practices
• Beginner guidance
• Safety & precautions

Try Asking:
• "What is Downward Dog?"
• "Benefits of yoga?"
• "How to start yoga?"
• "Poses for flexibility?"
• "Breathing techniques?"

Ask a yoga question and let's get started!"""


def answer_yoga_question(query: str, vector_db, llm) -> dict:
    if not is_yoga_question(query):
        return {
            "answer": "I'm a yoga specialist! Please ask yoga-related questions.\n\nExamples: What is Downward Dog? Benefits of yoga? How to start?",
            "sources": []
        }
    
    retriever = vector_db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    
    pose_match = re.search(r'#?(\d+)|pose\s+#?(\d+)|number\s+#?(\d+)', query.lower())
    if pose_match:
        pose_num = pose_match.group(1) or pose_match.group(2) or pose_match.group(3)
        docs = retriever.invoke(f"YOGA POSE #{pose_num}")
    else:
        docs = retriever.invoke(query)
    
    if docs and len(docs) > 0:
        context = docs[0].page_content
        
        if llm is not None:
            try:
                prompt = f"""You are an expert yoga instructor. Answer the user's question using ONLY the information provided in the context below. Do NOT make up information or reference other poses.

CONTEXT (Use ONLY this information):
{context}

USER QUESTION: {query}

INSTRUCTIONS:
1. Answer using ONLY the context above
2. If the context doesn't have the answer, say "I don't have specific information about that"
3. Include the pose name (English & Sanskrit if available)
4. List benefits, precautions, and techniques from the context
5. Be clear and concise
6. Do NOT mention other poses unless they are in the context

Answer:"""
                
                response = llm.invoke(prompt)
                
                if isinstance(response, dict):
                    for key in ['generated_text', 'text', 'output', 'answer']:
                        if key in response:
                            response = response[key]
                            break
                
                answer = str(response).strip()
                
                if not answer or len(answer) < 50:
                    answer = f"Based on the yoga knowledge base:\n\n{context}"
                elif "i don't know" in answer.lower() or "i cannot" in answer.lower():
                    answer = f"Based on the yoga knowledge base:\n\n{context}"
                
            except Exception as e:
                answer = f"Based on the yoga knowledge base:\n\n{context}"
        else:
            answer = f"Based on the yoga knowledge base:\n\n{context}"
    else:
        answer = generate_fallback_response(query)
    
    return {"answer": answer, "sources": docs}


st.set_page_config(
    page_title="Yoga Chatbot",
    page_icon="🧘",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .main-header { 
            text-align: center; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            font-size: 2.8em; 
            font-weight: bold;
            margin-bottom: 5px; 
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 8px 16px rgba(102, 126, 234, 0.4);
        }
        .sub-header { 
            text-align: center; 
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white; 
            font-size: 1.2em; 
            margin-bottom: 25px;
            padding: 12px;
            border-radius: 10px;
        }
        .answer-box { 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 20%, #f093fb 100%);
            border-left: 6px solid #667eea; 
            padding: 25px; 
            border-radius: 12px; 
            margin: 20px 0;
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
            color: white;
            font-size: 1.05em;
            line-height: 1.6;
        }
    </style>
""", unsafe_allow_html=True)


def main():
    st.markdown('<h1 class="main-header">Yoga Chatbot</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your personal yoga guide - ask anything about poses, benefits & techniques!</p>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    color: white; padding: 20px; border-radius: 10px; text-align: center;">
        <h2 style="margin: 0; font-size: 1.8em;">Yoga Expert</h2>
        <p style="margin: 5px 0; font-size: 0.9em;">Powered by Mistral-Large AI</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("")
        st.markdown("""
        ### Learn About
        • 1000+ Yoga Poses with details
        • Health Benefits & improvements
        • Breathing Techniques (Pranayama)
        • Meditation practices
        • Beginner to Advanced levels
        
        ### Key Features
        • AI-powered answers (Mistral-Large)
        • Accurate pose information
        • Safety precautions included
        • Sanskrit & English names
        • Step-by-step instructions
        
        ### Tips for Best Results
        • Be specific in questions
        • Ask about specific poses
        • Request step-by-step instructions
        • Ask for beginner guidance
        • Ask about benefits & contraindications
        """)
    
    try:
        with st.spinner("Loading yoga knowledge..."):
            chunks = load_yoga_data()
            db = create_vector_database(chunks)
            llm = setup_llm()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.stop()
    
    st.markdown("---")
    
    question = st.text_input(
        "Ask me about yoga:",
        placeholder="e.g., Downward Dog benefits? Beginner poses? How to start?",
        help="Ask any yoga question"
    )
    
    if question:
        is_safe, msg = check_safety(question)
        
        if not is_safe:
            st.warning(f"Blocked: {msg}")
        else:
            with st.spinner("Searching yoga knowledge..."):
                result = answer_yoga_question(question, db, llm)
                answer = result["answer"]
                sources = result["sources"]
            
            st.markdown('<div class="answer-box">', unsafe_allow_html=True)
            st.markdown(f"### Answer\n\n{answer}")
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #999; font-size: 0.85em; margin-top: 40px;">
    <p><b>Yoga Chatbot v1.0</b> | Powered by AI & RAG Technology</p>
    <p>Always consult certified instructors for personalized guidance</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
