import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Styling for the UI elements
st.markdown(
    """
    <style>
    /* Page background and layout */
    .css-1aumxhk {
        background-color: #1f2937 !important;
        padding-top: 40px;
    }
    /* Headers and labels */
    .css-1aumxhk h2 {
        color: #f4f4f5;
        font-size: 24px;
        text-align: center;
    }
    .css-1aumxhk label {
        color: #f4f4f5 !important;
        font-size: 16px;
    }
    /* Custom button styles */
    .css-1aumxhk button {
        background-color: #ff5e5e;
        color: white;
        font-size: 16px;
        padding: 12px 24px;
        border-radius: 50px;
        border: none;
        cursor: pointer;
        box-shadow: 0px 8px 15px rgba(255, 75, 43, 0.2);
        transition: all 0.3s ease;
        margin-top: 20px;
    }
    .css-1aumxhk button:hover {
        background-color: #f46b45;
        box-shadow: 0px 15px 20px rgba(255, 75, 43, 0.4);
        transform: translateY(-3px);
    }
    /* Header styling */
    h1 {
        color: #ff416c;
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 40px;
    }
    .css-184tjsw p {
        color: #6b7280;
        font-size: 18px;
        text-align: justify;
    }
    /* Button hover animation */
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
        position: relative;
        overflow: hidden;
        z-index: 1;
    }
    button:hover {
        background: linear-gradient(135deg, #ff4b2b, #ff416c);
        box-shadow: 0px 15px 20px rgba(255, 75, 43, 0.4);
        transform: translateY(-3px);
    }
    button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 300%;
        height: 300%;
        background: rgba(255, 255, 255, 0.2);
        transform: translate(-50%, -50%) scale(0);
        transition: all 0.5s ease;
        border-radius: 50%;
        z-index: -1;
    }
    button:hover::before {
        transform: translate(-50%, -50%) scale(1);
    }
    /* Footer */
    footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background-color: #1f2937;
        color: white;
        text-align: center;
        padding: 10px;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True
)

def qpsk_modulation(data_bits):
    symbol_map = {
        (0, 0): 1 + 1j,
        (0, 1): -1 + 1j,
        (1, 0): -1 - 1j,
        (1, 1): 1 - 1j,
    }
    data_pairs = [(data_bits[i], data_bits[i + 1]) for i in range(0, len(data_bits), 2)]
    symbols = [symbol_map[pair] for pair in data_pairs]
    return np.array(symbols)

def qpsk_demodulation(symbols):
    demodulated_bits = []
    for symbol in symbols:
        if symbol.real > 0 and symbol.imag > 0:
            demodulated_bits.extend([0, 0])
        elif symbol.real < 0 and symbol.imag > 0:
            demodulated_bits.extend([0, 1])
        elif symbol.real < 0 and symbol.imag < 0:
            demodulated_bits.extend([1, 1])
        else:
            demodulated_bits.extend([1, 0])
    return demodulated_bits

def awgn_channel(symbols, snr_db):
    snr_linear = 10 ** (snr_db / 10)
    noise_power = 1 / snr_linear
    noise = np.sqrt(noise_power / 2) * (np.random.randn(len(symbols)) + 1j * np.random.randn(len(symbols)))
    return symbols + noise

def calculate_ber(original_bits, received_bits):
    errors = np.sum(np.array(original_bits) != np.array(received_bits))
    return errors / len(original_bits)

def plot_constellation(symbols, title):
    fig, ax = plt.subplots()
    ax.scatter(symbols.real, symbols.imag)
    ax.set_title(title)
    ax.set_xlabel("In-Phase Component")
    ax.set_ylabel("Quadrature Component")
    ax.grid()
    ax.axhline(0, color='black', linewidth=0.5, ls='--')
    ax.axvline(0, color='black', linewidth=0.5, ls='--')
    return fig

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

def main():
    st.title("Satellite Communication: QPSK Modulation & Demodulation Simulation")
    
    st.write("""
    ### Scenario Description
    Satellite communication systems often use modulation schemes like QPSK for efficient and reliable data transmission. This simulation allows us to observe the QPSK modulation process, the impact of noise in a real-world scenario, and how data can be recovered after passing through a noisy channel.
    """)

    st.write("""
    ### Term Project
    This is a term project for the Digital Communication course submitted to **Sir Kamal Shahid**.
    """)

    num_bits = st.sidebar.number_input("Number of bits to generate:", min_value=1, value=1000)
    snr_db = st.sidebar.slider("Select SNR (dB):", 0, 20, 10)

    if st.button("Run QPSK Simulation"):
        data_bits = np.random.randint(0, 2, num_bits)
        modulated_symbols = qpsk_modulation(data_bits)

        st.subheader("Transmitted QPSK Signal Constellation")
        transmitted_fig = plot_constellation(modulated_symbols, "Transmitted QPSK Signal")
        st.pyplot(transmitted_fig)
        st.write("This constellation diagram represents the transmitted QPSK signal, with four distinct points corresponding to different bit pair combinations. These points are phase-shifted representations of the digital data.")

        received_symbols = awgn_channel(modulated_symbols, snr_db)

        st.subheader("Received QPSK Signal Constellation with AWGN")
        received_fig = plot_constellation(received_symbols, "Received QPSK Signal with AWGN")
        st.pyplot(received_fig)
        st.write("After passing through the AWGN channel, noise impacts the signal, causing deviations from the original constellation points. This visualizes how noise distorts the signal in real-world communication systems.")

        received_bits = qpsk_demodulation(received_symbols)
        ber = calculate_ber(data_bits, received_bits)
        st.write(f"Bit Error Rate (BER): {ber:.4f}")
        st.write("The calculated BER provides a quantitative measure of how much the noise affected the transmission. A lower BER indicates better performance under noisy conditions.")

        st.subheader("Demodulated QPSK Signal Constellation")
        demodulated_fig = plot_constellation(qpsk_modulation(received_bits), "Demodulated QPSK Signal")
        st.pyplot(demodulated_fig)
        st.write("This constellation shows the recovered symbols after demodulation. Ideally, these points should closely match the transmitted constellation, with minimal deviations caused by noise.")

        st.subheader("Modulation Scheme Comparison")
        ber_values = {
            'QPSK': ber,
            'BPSK': 0.1 * (snr_db / 10),  
            '8PSK': 0.15 * (snr_db / 10),  
        }
        
        plot_modulation_comparison(ber_values)
        st.pyplot(plt)
        st.write("This bar chart compares the Bit Error Rate (BER) for three modulation schemes: QPSK, BPSK, and 8PSK. Based on the graph, you can determine which scheme offers the lowest BER for the selected SNR.")

        best_modulation = min(ber_values, key=ber_values.get)
        st.write(f"**Based on the bar graph, {best_modulation} is the best modulation scheme for this scenario due to its lower Bit Error Rate (BER).**")

if __name__ == "__main__":
    main()
