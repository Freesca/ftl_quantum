from dotenv import load_dotenv
from qiskit_ibm_runtime import QiskitRuntimeService
import os
import sys

def main():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    # Per IBM Quantum Platform (free) di solito è "ibm-q/open/main".
    # Se usi IBM Cloud, metti nel .env la tua instance CRN e cambia il channel in 'ibm_cloud'.
    instance = os.getenv("IBM_INSTANCE", "ibm-q/open/main")
    channel = os.getenv("IBM_CHANNEL", "ibm_quantum_platform")  # oppure 'ibm_cloud'

    if not api_key:
        print("API key not found. Set API_KEY in your .env.")
        sys.exit(1)

    try:
        QiskitRuntimeService.save_account(
            channel=channel,
            token=api_key,
            instance=instance,   # <<--- importante!
            overwrite=True
        )
        print("API key saved successfully.")
    except Exception as e:
        print(f"Error saving API key: {e}")
        sys.exit(1)

    try:
        svc = QiskitRuntimeService(instance=instance)
        print(f"Using instance: {instance}")
        print([b.name for b in svc.backends()])
    except Exception as e:
        print(f"Error creating service/listing backends: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()