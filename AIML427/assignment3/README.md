# RT-IoT2022

Dataset:
https://www.kaggle.com/datasets/supplejade/rt-iot2022real-time-internet-of-things/data

Source paper:
https://www.semanticscholar.org/paper/Quantized-autoencoder-(QAE)-intrusion-detection-for-Sharmila-Nagapadma/753f6ede01b4acaa325e302c38f1e0c1ade74f5b

https://link.springer.com/article/10.1186/s42400-023-00178-5

The dataset is an Internet of Things network intrusion/attack dataset.

* number of features: 83
* data size: 52Mbytes
* row count: 123,118
* missing values: No.

The machine learning problem is to predict the attack given the data.

I will also investigate the features to see if there are dominant signals for each type of attack.


# Tasks

* Create a DecisionTree
* Prepare the data for PCA
* Train the DecisionTree on the PCA'ed data
* Training and _test_ accuracy
* Running time


* Run with
* Bare data
* Normalize the data
* Convert text features to 1-hot.
* Standardize + PCA + model

# Data Schema

The dataset has 5 columns which aren't pure numeric values.

## Attack_type

The label for the instance, text.

Attack Type, count
* NMAP\_FIN\_SCAN 28
* Metasploit\_Brute\_Force\_SSH 37
* Wipro\_bulb 253 - OK
* DDOS\_Slowloris 534
* NMAP\_TCP\_scan 1002
* NMAP\_OS\_DETECTION 2000
* NMAP\_XMAS\_TREE\_SCAN 2010
* NMAP\_UDP\_SCAN 2590
* MQTT\_Publish 4146 - OK
* ARP\_poisioning 7750
* Thing\_Speak 8108 - OK
* DOS\_SYN\_Hping 94659

The paper also lists "Amazon Alexa", but that isn't present in the labelled column.

## no

The row_id.

## id.orig_p

The originating port. Traffic is identified by {source\_port, destination\_port} this forms a soft (time localized) id.

Spans the address space, but also has substantial fan-in. That they aren't evenly distributed hints that this is good signal. Numeric.

## id.resp_p

The destination port. Traffic is identified by {source\_port, destination\_port} this forms a soft (time localized) id.

This is defined by the system being targetted, so has substantial fan-in. It will be correlated with the attack target. However, the service may run on other ports, so it does not drive subsystem. Numeric.

## proto

The protocol transporting the data. Text

* icmp
* tcp
* udp

## service

The system being connected to, text. The dataset says "no missing data", but "-" is recorded in this field. This probably indicates the server isn't running anything on that port. Given the NMAP TCP scans, this is expected. It should not be treated as missing data. Text.

* radius
* ssh
* irc
* dhcp
* ntp
* -
* ssl
* http
* mqtt
* dns


# Tasks

