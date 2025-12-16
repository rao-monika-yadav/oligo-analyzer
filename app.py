import streamlit as st
import pandas as pd
from io import StringIO
from typing import Optional, Dict, Union

# --- PART 1: Backend Logic ---
def calculate_metrics(dna_seq):
    dna_seq = dna_seq.upper()
    length = len(dna_seq)
    valid_bases = set("ATGCN")     #allows only valid characters
    
    if length == 0:
        return None

    if not set(dna_set).issubset(valid_bases):
        if not dna_seq.startswith(">"):
            return None
        
    a = dna_seq.count("A")
    t = dna_seq.count("T")
    g = dna_seq.count("G")
    c = dna_seq.count("C")
    
    # Standard Metrics
    tm = 4 * (g + c) + 2 * (a + t)   #wallace rule
    gc_per = round((g + c) / length * 100, 1)
    at_per = round((a + t) / length * 100, 1)
    
    # Molecular Weight Calculation (Daltons)
    # Weights: A=313.21, T=304.2, C=289.18, G=329.21 
    # -61.9 adjustment = for the phosphate removal at the 5' end
    mw = (a * 313.21) + (t * 304.2) + (c * 289.18) + (g * 329.21) - 61.96       # (approximate Molecular Weight of a single-stranded DNA oligo)

    return {
        "Length": length,
        "Tm (C)": tm,
        "GC%": gc_per,
        "AT%": at_per,
        "MW (Da)": round(mw, 2),
        "A_count": a,
        "T_count": t,
        "G_count": g,
        "C_count": c
    }

def get_reverse_complement(dna_seq):
    dna_seq = dna_seq.upper()
    complement_dict = {'A': 'T', 'C': 'G', 'T': 'A', 'G': 'C', 'N':'N'}
    complement_seq = ""
    for base in dna_seq:
        if base in complement_dict:
            complement_seq += complement_dict[base]
        else:
            complement_seq += "N"
    return complement_seq[::-1]

# --- PART 2: THE FRONTEND (UI) ---

# A. PAGE CONFIGURATION
st.set_page_config(
    page_title="Oligo Analyzer Pro", 
    page_icon="🧬", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# B. THE SIDEBAR (Branding Center)
with st.sidebar:
    logo_html = """
    <div style="
        width: 60px;
        height: 60px;
        background-color: #0068c9; 
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
    ">
        <span style="
            color: white;
            font-size: 24px;
            font-weight: bold;
            font-family: 'Lucida Handwriting', cursive;
            letter-spacing: 2px;
        ">MY</span>
    </div>
    """
    st.markdown(logo_html, unsafe_allow_html=True)
    
    st.title("Oligo Analyzer")
    st.caption("v1.0.0 | Bio-Tools Suite")
    st.markdown("---")
    
    # FUNCTIONALITY SECTION ---
    st.write("### 🛠️ Key Features")
    st.markdown("""
    - **Tm Calculation:** Uses the Wallace Rule for accurate melting temperatures.
    - **Quality Control:** Visualizes GC% and identifies unstable primers.
    - **Batch Processing:** Analyzes large FASTA files in seconds.
    - **Reverse Complement:** Instantly generates ordering sequences.
    """)
    
    st.markdown("---")
    
    # AUTHOR ---
    st.write("### 👨‍🔬 Author")
    st.markdown("**Monika Yadav**")
    st.caption("MSc Bioinformatics Candidate")
    st.caption("BSc (Hons.)/MSc Biotechnology")
    
    # CONTACT ME (Social Links) ---
    st.markdown(
        """
        <div style="display: flex; gap: 10px;">
            <a href="#" target="_blank">LinkedIn</a> • 
            <a href="https://github.com/rao-monika-yadav" target="_blank">GitHub</a> • 
            <a href="#">Email</a>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    st.warning("For Educational and Research Use Only")

# C. MAIN AREA
st.title("🧬 Oligo Analyzer Pro")
st.markdown("##### Professional grade primer analysis & batch processing.")

# D. THE "HOW TO" EXPANDER
with st.expander("📖 How to use this tool"):
    st.markdown("""
    1. **Single Sequence:** Paste a raw DNA string (A,T,C,G) to get instant metrics.
    2. **Bulk Analysis:** Upload a `.fasta` or `.txt` file containing multiple records.
    3. **Interpretation:**
        * **Tm (Melting Temp):** Aim for 50-60°C for standard PCR.
        * **GC%:** Ideal range is usually 40-60%.
    """)

# E. TABS (The Workspace)
tab1, tab2 = st.tabs(["🔍 Single Sequence", "📂 Bulk Analysis (Upload)"])

# === TAB 1: SINGLE SEQUENCE ===
with tab1:
    st.markdown("### Quick Check")
    col_input, col_action = st.columns([3, 1])
    
    with col_input:
        user_dna = st.text_input("Paste DNA sequence (5' -> 3'):", value="", help="Only A, T, C, G characters allowed.")
    
    with col_action:
        st.write("##") # Spacer
        analyze_btn = st.button("Analyze", type="primary", use_container_width=True)

    if analyze_btn:
        if user_dna:
            metrics = calculate_metrics(user_dna)
            
            if metrics is None:   #check if metrics came back as None
                st.error("INVALID SEQUENCE DETECTED! Please use only A, T, G, C, or N.")
            else:
                rev_comp = get_reverse_complement(user_dna)
            
                st.divider() # Visual separator
            
                # Display Metrics
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Melting Temp (Tm)", f"{metrics['Tm (C)']} °C", delta="Target: 55-60°C", delta_color="off")
                c2.metric("GC Content", f"{metrics['GC%']}%")
                c3.metric("AT Content", f"{metrics['AT%']}%")
                c4.metric("Mol Wt", f"{metrics['MW (Da)']} Da")
                
                # Visualization
                st.subheader("Nucleotide Composition")
                chart_data = pd.DataFrame({
                    'Nucleotide': ['A', 'T', 'G', 'C'],
                    'Count': [metrics['A_count'], metrics['T_count'], metrics['G_count'], metrics['C_count']]
                })
                st.bar_chart(chart_data.set_index('Nucleotide'), color="#0068c9") 
                
                # Reverse Complement
                st.subheader("Reverse Complement")
                st.code(rev_comp, language='text')
            else:
                st.error("Please enter a valid sequence.")

# === TAB 2: BULK ANALYSIS ===
with tab2:
    st.markdown("### Batch Processing")
    uploaded_file = st.file_uploader("Upload .fasta or .txt file", type=["fasta", "txt"])
    
    if uploaded_file is not None:
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        records = []
        current_seq = ""
        current_header = None
        
        for line in stringio:
            line = line.strip()
            if line.startswith(">"):
                if current_header:
                    stats = calculate_metrics(current_seq)
                    if stats:
                        stats["ID"] = current_header
                        stats["Sequence"] = current_seq
                        stats["Rev_Comp"] = get_reverse_complement(current_seq)
                        records.append(stats)
                current_header = line[1:]
                current_seq = ""
            else:
                current_seq += line
        
        if current_header:
             stats = calculate_metrics(current_seq)
             if stats:
                stats["ID"] = current_header
                stats["Sequence"] = current_seq
                stats["Rev_Comp"] = get_reverse_complement(current_seq)
                records.append(stats)
                
        if records:
            df = pd.DataFrame(records)
            cols = ["ID", "Length", "Tm (C)", "GC%", "AT%", "MW (Da)", "Sequence", "Rev_Comp"]
            df = df[cols]
            
            st.success(f"✅ Successfully processed {len(df)} sequences.")
            
            # Quality Control Plot
            st.subheader("Batch Quality Control")
            st.scatter_chart(
                df,
                x='GC%',
                y='Tm (C)',
                color='Length'
            )
            
            st.subheader("Data Table")
            st.dataframe(df, use_container_width=True)
            
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Report",
                data=csv,
                file_name="oligo_batch_results.csv",
                mime="text/csv",
                type="primary"

            )

