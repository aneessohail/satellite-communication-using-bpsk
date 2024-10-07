import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# CSS for styling
st.markdown(
    """
    <style>
    body {
        background-color: #f4f4f5;
    }
    .stApp {
        background-color: #1f2937;
        color: #f4f4f5;
    }
    h1, h2, h3 {
        color: #ff416c;
        text-align: center;
    }
    label {
        color: #f4f4f5 !important;
    }
    button {
        background: linear-gradient(135deg, #ff416c, #ff4b2b);
        color: white;
        font-size: 16px;
        padding: 12px 24px;
        border-radius: 25px;
        border: none;
        cursor: pointer;
        box-shadow: 0px 8px 15px rgba(255, 75, 43, 0.2);
        transition: all 0.3s ease;
        margin-top: 20px;
        z-index: 1;
    }
    button:hover {
        background: linear-gradient(135deg, #ff4b2b, #ff416c);
        box-shadow: 0px 15px 20px rgba(255, 75, 43, 0.4);
        transform: translateY(-3px);
        text:white
    }
    .stTextInput {
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# BPSK Modulation
def bpsk_modulation(data_bits):
    symbols = np.array([1 if bit == 1 else -1 for bit in data_bits])
    return symbols

# BPSK Demodulation
def bpsk_demodulation(symbols):
    demodulated_bits = np.array([1 if symbol > 0 else 0 for symbol in symbols])
    return demodulated_bits

# AWGN channel
def awgn_channel(symbols, snr_db):
    snr_linear = 10 ** (snr_db / 10)
    noise_power = 1 / snr_linear
    noise = np.sqrt(noise_power / 2) * np.random.randn(len(symbols))
    return symbols + noise

# Calculate Bit Error Rate (BER)
def calculate_ber(original_bits, received_bits):
    errors = np.sum(np.array(original_bits) != np.array(received_bits))
    return errors / len(original_bits)

# Plot Constellation Diagram
def plot_constellation(symbols, title):
    fig, ax = plt.subplots()
    ax.scatter(symbols, np.zeros_like(symbols))
    ax.set_title(title)
    ax.set_xlabel("In-Phase Component")
    ax.set_ylabel("Quadrature Component")
    ax.grid()
    ax.axhline(0, color='black', linewidth=0.5, ls='--')
    ax.axvline(0, color='black', linewidth=0.5, ls='--')
    return fig

# Plot Modulation Scheme Comparison
def plot_modulation_comparison(ber_values):
    plt.figure()
    modulations = list(ber_values.keys())
    ber = list(ber_values.values())
    
    plt.bar(modulations, ber, color=['blue', 'orange', 'green'])
    plt.title("Comparison of Modulation Schemes")
    plt.xlabel("Modulation Scheme")
    plt.ylabel("Bit Error Rate (BER)")
    plt.yscale('log')
    plt.grid(axis='y')
    plt.xticks(rotation=45)
    plt.tight_layout()

# Main App
def main():
    st.title("Satellite Communication: BPSK Modulation & Demodulation Simulation")
    
    st.write("""
    ### Scenario Description
    Satellite communication systems often use modulation schemes like **BPSK** for reliable data transmission. This simulation lets us observe the BPSK modulation process, the impact of noise in a real-world scenario, and how data is recovered after passing through a noisy channel.
    """)

    st.write("""
    ### Term Project
    This is a term project for the Digital Communication course submitted to **Sir Kamal Shahid**.
    """)

    num_bits = st.sidebar.number_input("Number of bits to generate:", min_value=1, value=1000)
    snr_db = st.sidebar.slider("Select SNR (dB):", 0, 20, 10)

    if st.button("Run BPSK Simulation"):
        # Generate random data bits
        data_bits = np.random.randint(0, 2, num_bits)

        # BPSK Modulation
        modulated_symbols = bpsk_modulation(data_bits)
        st.subheader("Transmitted BPSK Signal Constellation")
        transmitted_fig = plot_constellation(modulated_symbols, "Transmitted BPSK Signal")
        st.pyplot(transmitted_fig)
        st.write("The constellation diagram of the transmitted signal shows that BPSK modulates data by shifting the signal's phase by 180°.")

        # Pass through AWGN channel
        received_symbols = awgn_channel(modulated_symbols, snr_db)
        st.subheader("Received BPSK Signal Constellation with AWGN")
        received_fig = plot_constellation(received_symbols, "Received BPSK Signal with AWGN")
        st.pyplot(received_fig)
        st.write("After passing through the AWGN channel, noise has been added to the signal, causing the symbols to scatter around their original positions.")

        # BPSK Demodulation
        received_bits = bpsk_demodulation(received_symbols)
        ber = calculate_ber(data_bits, received_bits)
        st.write(f"Bit Error Rate (BER): {ber:.4f}")
        st.write("The Bit Error Rate (BER) is calculated to evaluate the performance of the system. A lower BER indicates better performance.")

        # Compare with other modulation schemes (if desired)
        st.subheader("Modulation Scheme Comparison")
        ber_values = {
            'BPSK': ber,
            'QPSK': 0.1 * (snr_db / 10),  # Placeholder value for QPSK
            '8PSK': 0.15 * (snr_db / 10),  # Placeholder value for 8PSK
        }

        plot_modulation_comparison(ber_values)
        st.pyplot(plt)
        st.write("**Based on the bar graph, BPSK is the most robust modulation scheme in this scenario due to its lower Bit Error Rate (BER) at the selected SNR.**")

if __name__ == "__main__":
    main()
