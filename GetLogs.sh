#/bin/bash


MSG="GET /healthcheck"
namespaces=('nf-amf' 'nf-nrf' 'nf-smf' 'nf-pcrf')
#namespaces=$(microk8s kubectl get namespaces | grep -E 'mf|nrf|pcrf' | tr -s " " | cut -d" " -f1 | tr '\n' ' ')
OUTPUT="./logs/logs.txt"
rm -fr $OUTPUT


for NAMESPACE in "${namespaces[@]}"; do
        echo "PODS LOGS FROM THE NAMESPACE $NAMESPACE" >> $OUTPUT
        echo -e >> $OUTPUT
        POD=$(microk8s kubectl get pods -n $NAMESPACE | tr -s " " | cut -d" " -f1 | tail -n1)
        microk8s kubectl logs $POD -n $NAMESPACE | grep -v "$MSG" >> $OUTPUT
        echo -e "===========================================================================================================================================================" >> $OUTPUT
        echo -e >> $OUTPUT
        echo -e >> $OUTPUT
        echo -e >> $OUTPUT
done

