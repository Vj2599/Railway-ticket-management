import os
import django
from datetime import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'railway_project.settings')
django.setup()

from railway_app.models import Station, Train, Route, Schedule

def populate_stations():
    """Populate major Indian railway stations"""
    stations_data = [
        # Delhi NCR
        {'code': 'NDLS', 'name': 'New Delhi', 'city': 'Delhi', 'state': 'Delhi'},
        {'code': 'DLI', 'name': 'Delhi Junction', 'city': 'Delhi', 'state': 'Delhi'},
        {'code': 'NZM', 'name': 'Hazrat Nizamuddin', 'city': 'Delhi', 'state': 'Delhi'},
        {'code': 'ANVT', 'name': 'Anand Vihar Terminal', 'city': 'Delhi', 'state': 'Delhi'},
        {'code': 'GZB', 'name': 'Ghaziabad Junction', 'city': 'Ghaziabad', 'state': 'Uttar Pradesh'},
        {'code': 'Noida', 'name': 'Noida Sector 15', 'city': 'Noida', 'state': 'Uttar Pradesh'},

        # Uttar Pradesh
        {'code': 'LKO', 'name': 'Lucknow Junction', 'city': 'Lucknow', 'state': 'Uttar Pradesh'},
        {'code': 'CNB', 'name': 'Kanpur Central', 'city': 'Kanpur', 'state': 'Uttar Pradesh'},
        {'code': 'ALD', 'name': 'Allahabad Junction', 'city': 'Prayagraj', 'state': 'Uttar Pradesh'},
        {'code': 'VGLB', 'name': 'Virangana Lakshmibai Junction', 'city': 'Jhansi', 'state': 'Uttar Pradesh'},
        {'code': 'AGC', 'name': 'Agra Cantonment', 'city': 'Agra', 'state': 'Uttar Pradesh'},
        {'code': 'MB', 'name': 'Moradabad Junction', 'city': 'Moradabad', 'state': 'Uttar Pradesh'},
        {'code': 'BE', 'name': 'Bareilly Junction', 'city': 'Bareilly', 'state': 'Uttar Pradesh'},
        {'code': 'GD', 'name': 'Gonda Junction', 'city': 'Gonda', 'state': 'Uttar Pradesh'},
        {'code': 'BST', 'name': 'Basti', 'city': 'Basti', 'state': 'Uttar Pradesh'},
        {'code': 'GKP', 'name': 'Gorakhpur Junction', 'city': 'Gorakhpur', 'state': 'Uttar Pradesh'},
        {'code': 'LJN', 'name': 'Lucknow Junction NER', 'city': 'Lucknow', 'state': 'Uttar Pradesh'},
        {'code': 'SPN', 'name': 'Shahjahanpur', 'city': 'Shahjahanpur', 'state': 'Uttar Pradesh'},
        {'code': 'HRI', 'name': 'Hardoi', 'city': 'Hardoi', 'state': 'Uttar Pradesh'},

        # Bihar
        {'code': 'PNBE', 'name': 'Patna Junction', 'city': 'Patna', 'state': 'Bihar'},
        {'code': 'PPTA', 'name': 'Patliputra Junction', 'city': 'Patna', 'state': 'Bihar'},
        {'code': 'BJU', 'name': 'Barauni Junction', 'city': 'Barauni', 'state': 'Bihar'},
        {'code': 'MFP', 'name': 'Muzaffarpur Junction', 'city': 'Muzaffarpur', 'state': 'Bihar'},
        {'code': 'SPJ', 'name': 'Samastipur Junction', 'city': 'Samastipur', 'state': 'Bihar'},
        {'code': 'DNR', 'name': 'Danapur', 'city': 'Danapur', 'state': 'Bihar'},
        {'code': 'ARA', 'name': 'Ara Junction', 'city': 'Ara', 'state': 'Bihar'},
        {'code': 'BXR', 'name': 'Buxar', 'city': 'Buxar', 'state': 'Bihar'},
        {'code': 'GAYA', 'name': 'Gaya Junction', 'city': 'Gaya', 'state': 'Bihar'},
        {'code': 'KIUL', 'name': 'Kiul Junction', 'city': 'Kiul', 'state': 'Bihar'},

        # West Bengal
        {'code': 'HWH', 'name': 'Howrah Junction', 'city': 'Kolkata', 'state': 'West Bengal'},
        {'code': 'KOAA', 'name': 'Kolkata', 'city': 'Kolkata', 'state': 'West Bengal'},
        {'code': 'SDAH', 'name': 'Sealdah', 'city': 'Kolkata', 'state': 'West Bengal'},
        {'code': 'ASN', 'name': 'Asansol Junction', 'city': 'Asansol', 'state': 'West Bengal'},
        {'code': 'DHN', 'name': 'Dhanbad Junction', 'city': 'Dhanbad', 'state': 'Jharkhand'},
        {'code': 'RNC', 'name': 'Ranchi Junction', 'city': 'Ranchi', 'state': 'Jharkhand'},
        {'code': 'TATA', 'name': 'Tatanagar Junction', 'city': 'Jamshedpur', 'state': 'Jharkhand'},
        {'code': 'KGP', 'name': 'Kharagpur Junction', 'city': 'Kharagpur', 'state': 'West Bengal'},
        {'code': 'BQA', 'name': 'Bankura', 'city': 'Bankura', 'state': 'West Bengal'},
        {'code': 'MDN', 'name': 'Midnapore', 'city': 'Midnapore', 'state': 'West Bengal'},

        # Maharashtra
        {'code': 'BCT', 'name': 'Mumbai Central', 'city': 'Mumbai', 'state': 'Maharashtra'},
        {'code': 'CST', 'name': 'Chhatrapati Shivaji Terminus', 'city': 'Mumbai', 'state': 'Maharashtra'},
        {'code': 'CSTM', 'name': 'Mumbai CST', 'city': 'Mumbai', 'state': 'Maharashtra'},
        {'code': 'DR', 'name': 'Dadar Central', 'city': 'Mumbai', 'state': 'Maharashtra'},
        {'code': 'TNA', 'name': 'Thane', 'city': 'Thane', 'state': 'Maharashtra'},
        {'code': 'KYN', 'name': 'Kalyan Junction', 'city': 'Kalyan', 'state': 'Maharashtra'},
        {'code': 'KJT', 'name': 'Karjat Junction', 'city': 'Karjat', 'state': 'Maharashtra'},
        {'code': 'LNL', 'name': 'Lonavala', 'city': 'Lonavala', 'state': 'Maharashtra'},
        {'code': 'PUNE', 'name': 'Pune Junction', 'city': 'Pune', 'state': 'Maharashtra'},
        {'code': 'DD', 'name': 'Daund Junction', 'city': 'Daund', 'state': 'Maharashtra'},
        {'code': 'SUR', 'name': 'Solapur Junction', 'city': 'Solapur', 'state': 'Maharashtra'},
        {'code': 'NAGPUR', 'name': 'Nagpur Junction', 'city': 'Nagpur', 'state': 'Maharashtra'},
        {'code': 'GONDIA', 'name': 'Gondia Junction', 'city': 'Gondia', 'state': 'Maharashtra'},
        {'code': 'NGP', 'name': 'Nagpur', 'city': 'Nagpur', 'state': 'Maharashtra'},
        {'code': 'AMI', 'name': 'Amravati', 'city': 'Amravati', 'state': 'Maharashtra'},
        {'code': 'AK', 'name': 'Akola Junction', 'city': 'Akola', 'state': 'Maharashtra'},
        {'code': 'BSL', 'name': 'Bhusaval Junction', 'city': 'Bhusaval', 'state': 'Maharashtra'},
        {'code': 'JL', 'name': 'Jalgaon Junction', 'city': 'Jalgaon', 'state': 'Maharashtra'},
        {'code': 'NK', 'name': 'Nasik Road', 'city': 'Nashik', 'state': 'Maharashtra'},
        {'code': 'IGP', 'name': 'Igatpuri', 'city': 'Igatpuri', 'state': 'Maharashtra'},

        # Gujarat
        {'code': 'ADI', 'name': 'Ahmedabad Junction', 'city': 'Ahmedabad', 'state': 'Gujarat'},
        {'code': 'BRC', 'name': 'Vadodara Junction', 'city': 'Vadodara', 'state': 'Gujarat'},
        {'code': 'ST', 'name': 'Surat', 'city': 'Surat', 'state': 'Gujarat'},
        {'code': 'BVI', 'name': 'Borivali', 'city': 'Mumbai', 'state': 'Maharashtra'},
        {'code': 'VAPI', 'name': 'Vapi', 'city': 'Vapi', 'state': 'Gujarat'},
        {'code': 'BL', 'name': 'Valsad', 'city': 'Valsad', 'state': 'Gujarat'},
        {'code': 'NVS', 'name': 'Navsari', 'city': 'Navsari', 'state': 'Gujarat'},
        {'code': 'UDN', 'name': 'Udhna Junction', 'city': 'Surat', 'state': 'Gujarat'},
        {'code': 'ANND', 'name': 'Anand Junction', 'city': 'Anand', 'state': 'Gujarat'},
        {'code': 'BH', 'name': 'Bharuch Junction', 'city': 'Bharuch', 'state': 'Gujarat'},

        # Rajasthan
        {'code': 'JP', 'name': 'Jaipur Junction', 'city': 'Jaipur', 'state': 'Rajasthan'},
        {'code': 'JU', 'name': 'Jodhpur Junction', 'city': 'Jodhpur', 'state': 'Rajasthan'},
        {'code': 'AII', 'name': 'Ajmer Junction', 'city': 'Ajmer', 'state': 'Rajasthan'},
        {'code': 'BKN', 'name': 'Bikaner Junction', 'city': 'Bikaner', 'state': 'Rajasthan'},
        {'code': 'KOTA', 'name': 'Kota Junction', 'city': 'Kota', 'state': 'Rajasthan'},
        {'code': 'RTM', 'name': 'Ratlam Junction', 'city': 'Ratlam', 'state': 'Madhya Pradesh'},
        {'code': 'UDZ', 'name': 'Udaipur City', 'city': 'Udaipur', 'state': 'Rajasthan'},
        {'code': 'SWM', 'name': 'Sawai Madhopur', 'city': 'Sawai Madhopur', 'state': 'Rajasthan'},
        {'code': 'BHL', 'name': 'Bhilwara', 'city': 'Bhilwara', 'state': 'Rajasthan'},
        {'code': 'COR', 'name': 'Chittaurgarh', 'city': 'Chittaurgarh', 'state': 'Rajasthan'},

        # Madhya Pradesh
        {'code': 'BPL', 'name': 'Bhopal Junction', 'city': 'Bhopal', 'state': 'Madhya Pradesh'},
        {'code': 'JBP', 'name': 'Jabalpur Junction', 'city': 'Jabalpur', 'state': 'Madhya Pradesh'},
        {'code': 'ET', 'name': 'Itarsi Junction', 'city': 'Itarsi', 'state': 'Madhya Pradesh'},
        {'code': 'NAD', 'name': 'Nagda Junction', 'city': 'Nagda', 'state': 'Madhya Pradesh'},
        {'code': 'UJN', 'name': 'Ujjain Junction', 'city': 'Ujjain', 'state': 'Madhya Pradesh'},
        {'code': 'INDB', 'name': 'Indore Junction BG', 'city': 'Indore', 'state': 'Madhya Pradesh'},
        {'code': 'GWL', 'name': 'Gwalior Junction', 'city': 'Gwalior', 'state': 'Madhya Pradesh'},
        {'code': 'MRA', 'name': 'Morena', 'city': 'Morena', 'state': 'Madhya Pradesh'},
        {'code': 'SGO', 'name': 'Saugor', 'city': 'Saugor', 'state': 'Madhya Pradesh'},
        {'code': 'DMO', 'name': 'Damoh', 'city': 'Damoh', 'state': 'Madhya Pradesh'},

        # Karnataka
        {'code': 'SBC', 'name': 'Bangalore City', 'city': 'Bangalore', 'state': 'Karnataka'},
        {'code': 'YPR', 'name': 'Yesvantpur Junction', 'city': 'Bangalore', 'state': 'Karnataka'},
        {'code': 'MYS', 'name': 'Mysore Junction', 'city': 'Mysore', 'state': 'Karnataka'},
        {'code': 'UBL', 'name': 'Hubli Junction', 'city': 'Hubli', 'state': 'Karnataka'},
        {'code': 'DWR', 'name': 'Dharwad', 'city': 'Dharwad', 'state': 'Karnataka'},
        {'code': 'BGM', 'name': 'Belgaum', 'city': 'Belgaum', 'state': 'Karnataka'},
        {'code': 'MRJ', 'name': 'Miraj Junction', 'city': 'Miraj', 'state': 'Maharashtra'},
        {'code': 'PVR', 'name': 'Pandharpur', 'city': 'Pandharpur', 'state': 'Maharashtra'},
        {'code': 'GR', 'name': 'Gulbarga', 'city': 'Gulbarga', 'state': 'Karnataka'},
        {'code': 'WADI', 'name': 'Wadi Junction', 'city': 'Wadi', 'state': 'Karnataka'},
        {'code': 'YG', 'name': 'Yadgir', 'city': 'Yadgir', 'state': 'Karnataka'},
        {'code': 'RC', 'name': 'Raichur Junction', 'city': 'Raichur', 'state': 'Karnataka'},
        {'code': 'MALM', 'name': 'Manthralayam Road', 'city': 'Manthralayam', 'state': 'Andhra Pradesh'},
        {'code': 'AD', 'name': 'Adoni', 'city': 'Adoni', 'state': 'Andhra Pradesh'},
        {'code': 'GTL', 'name': 'Guntakal Junction', 'city': 'Guntakal', 'state': 'Andhra Pradesh'},
        {'code': 'BAY', 'name': 'Bellary Junction', 'city': 'Bellary', 'state': 'Karnataka'},
        {'code': 'HPT', 'name': 'Hosapete Junction', 'city': 'Hosapete', 'state': 'Karnataka'},
        {'code': 'KBL', 'name': 'Koppal', 'city': 'Koppal', 'state': 'Karnataka'},
        {'code': 'GDG', 'name': 'Gadag Junction', 'city': 'Gadag', 'state': 'Karnataka'},
        {'code': 'BGK', 'name': 'Bagalkot', 'city': 'Bagalkot', 'state': 'Karnataka'},

        # Andhra Pradesh & Telangana
        {'code': 'MAS', 'name': 'Chennai Central', 'city': 'Chennai', 'state': 'Tamil Nadu'},
        {'code': 'TPTY', 'name': 'Tirupati', 'city': 'Tirupati', 'state': 'Andhra Pradesh'},
        {'code': 'RU', 'name': 'Renigunta Junction', 'city': 'Renigunta', 'state': 'Andhra Pradesh'},
        {'code': 'KPD', 'name': 'Katpadi Junction', 'city': 'Vellore', 'state': 'Tamil Nadu'},
        {'code': 'JTJ', 'name': 'Jolarpettai', 'city': 'Jolarpettai', 'state': 'Tamil Nadu'},
        {'code': 'KJM', 'name': 'Krishnarajapuram', 'city': 'Bangalore', 'state': 'Karnataka'},
        {'code': 'BZA', 'name': 'Vijayawada Junction', 'city': 'Vijayawada', 'state': 'Andhra Pradesh'},
        {'code': 'GNT', 'name': 'Guntur Junction', 'city': 'Guntur', 'state': 'Andhra Pradesh'},
        {'code': 'NRT', 'name': 'Narasaraopet', 'city': 'Narasaraopet', 'state': 'Andhra Pradesh'},
        {'code': 'MRK', 'name': 'Markapur Road', 'city': 'Markapur', 'state': 'Andhra Pradesh'},
        {'code': 'NDL', 'name': 'Nandyal Junction', 'city': 'Nandyal', 'state': 'Andhra Pradesh'},
        {'code': 'DHNE', 'name': 'Dhone Junction', 'city': 'Dhone', 'state': 'Andhra Pradesh'},
        {'code': 'GY', 'name': 'Gooty Junction', 'city': 'Gooty', 'state': 'Andhra Pradesh'},
        {'code': 'VSKP', 'name': 'Visakhapatnam', 'city': 'Visakhapatnam', 'state': 'Andhra Pradesh'},
        {'code': 'DVD', 'name': 'Duvvada', 'city': 'Visakhapatnam', 'state': 'Andhra Pradesh'},
        {'code': 'AKP', 'name': 'Anakapalle', 'city': 'Anakapalle', 'state': 'Andhra Pradesh'},
        {'code': 'TUNI', 'name': 'Tuni', 'city': 'Tuni', 'state': 'Andhra Pradesh'},
        {'code': 'RJY', 'name': 'Rajahmundry', 'city': 'Rajahmundry', 'state': 'Andhra Pradesh'},
        {'code': 'NDD', 'name': 'Nidadavolu', 'city': 'Nidadavolu', 'state': 'Andhra Pradesh'},
        {'code': 'TDD', 'name': 'Tadepalligudem', 'city': 'Tadepalligudem', 'state': 'Andhra Pradesh'},
        {'code': 'EE', 'name': 'Eluru', 'city': 'Eluru', 'state': 'Andhra Pradesh'},
        {'code': 'HYB', 'name': 'Hyderabad Deccan', 'city': 'Hyderabad', 'state': 'Telangana'},
        {'code': 'SC', 'name': 'Secunderabad Junction', 'city': 'Hyderabad', 'state': 'Telangana'},
        {'code': 'NZB', 'name': 'Nizamabad Junction', 'city': 'Nizamabad', 'state': 'Telangana'},
        {'code': 'MCI', 'name': 'Mancherial', 'city': 'Mancherial', 'state': 'Telangana'},
        {'code': 'BPQ', 'name': 'Balharshah', 'city': 'Balharshah', 'state': 'Maharashtra'},
        {'code': 'CD', 'name': 'Chandrapur', 'city': 'Chandrapur', 'state': 'Maharashtra'},
        {'code': 'WL', 'name': 'Warangal', 'city': 'Warangal', 'state': 'Telangana'},
        {'code': 'KMT', 'name': 'Khammam', 'city': 'Khammam', 'state': 'Telangana'},
        {'code': 'DKJ', 'name': 'Dornakal Junction', 'city': 'Dornakal', 'state': 'Telangana'},

        # Tamil Nadu
        {'code': 'MS', 'name': 'Chennai Egmore', 'city': 'Chennai', 'state': 'Tamil Nadu'},
        {'code': 'TBM', 'name': 'Tambaram', 'city': 'Chennai', 'state': 'Tamil Nadu'},
        {'code': 'CGL', 'name': 'Chengalpattu Junction', 'city': 'Chengalpattu', 'state': 'Tamil Nadu'},
        {'code': 'VM', 'name': 'Villupuram Junction', 'city': 'Villupuram', 'state': 'Tamil Nadu'},
        {'code': 'TPJ', 'name': 'Tiruchchirappalli Junction', 'city': 'Tiruchchirappalli', 'state': 'Tamil Nadu'},
        {'code': 'MDU', 'name': 'Madurai Junction', 'city': 'Madurai', 'state': 'Tamil Nadu'},
        {'code': 'TEN', 'name': 'Tirunelveli', 'city': 'Tirunelveli', 'state': 'Tamil Nadu'},
        {'code': 'CBE', 'name': 'Coimbatore Junction', 'city': 'Coimbatore', 'state': 'Tamil Nadu'},
        {'code': 'SA', 'name': 'Salem Junction', 'city': 'Salem', 'state': 'Tamil Nadu'},
        {'code': 'ED', 'name': 'Erode Junction', 'city': 'Erode', 'state': 'Tamil Nadu'},

        # Kerala
        {'code': 'ERS', 'name': 'Ernakulam Junction', 'city': 'Kochi', 'state': 'Kerala'},
        {'code': 'TCR', 'name': 'Thrisur', 'city': 'Thrisur', 'state': 'Kerala'},
        {'code': 'CLT', 'name': 'Kozhikode', 'city': 'Kozhikode', 'state': 'Kerala'},
        {'code': 'CAN', 'name': 'Kannur', 'city': 'Kannur', 'state': 'Kerala'},
        {'code': 'TVC', 'name': 'Thiruvananthapuram Central', 'city': 'Thiruvananthapuram', 'state': 'Kerala'},
        {'code': 'QLN', 'name': 'Kollam Junction', 'city': 'Kollam', 'state': 'Kerala'},
        {'code': 'ALLP', 'name': 'Alappuzha', 'city': 'Alappuzha', 'state': 'Kerala'},
        {'code': 'SRTL', 'name': 'Cherthala', 'city': 'Cherthala', 'state': 'Kerala'},

        # Odisha
        {'code': 'BBS', 'name': 'Bhubaneswar', 'city': 'Bhubaneswar', 'state': 'Odisha'},
        {'code': 'PURI', 'name': 'Puri', 'city': 'Puri', 'state': 'Odisha'},
        {'code': 'CTC', 'name': 'Cuttack', 'city': 'Cuttack', 'state': 'Odisha'},
        {'code': 'BAM', 'name': 'Brahmapur', 'city': 'Brahmapur', 'state': 'Odisha'},
        {'code': 'PSA', 'name': 'Palasa', 'city': 'Palasa', 'state': 'Andhra Pradesh'},
        {'code': 'CHE', 'name': 'Srikakulam Road', 'city': 'Srikakulam', 'state': 'Andhra Pradesh'},
        {'code': 'VZM', 'name': 'Vizianagaram', 'city': 'Vizianagaram', 'state': 'Andhra Pradesh'},
        {'code': 'SBP', 'name': 'Sambalpur', 'city': 'Sambalpur', 'state': 'Odisha'},
        {'code': 'JSG', 'name': 'Jharsuguda Junction', 'city': 'Jharsuguda', 'state': 'Odisha'},
        {'code': 'ROU', 'name': 'Rourkela', 'city': 'Rourkela', 'state': 'Odisha'},

        # Chhattisgarh
        {'code': 'BILASPUR', 'name': 'Bilaspur Junction', 'city': 'Bilaspur', 'state': 'Chhattisgarh'},
        {'code': 'RAIPUR', 'name': 'Raipur Junction', 'city': 'Raipur', 'state': 'Chhattisgarh'},
        {'code': 'DURG', 'name': 'Durg Junction', 'city': 'Durg', 'state': 'Chhattisgarh'},
        {'code': 'NAB', 'name': 'Nagbhir Junction', 'city': 'Nagbhir', 'state': 'Maharashtra'},
        {'code': 'GAD', 'name': 'Gondia Junction', 'city': 'Gondia', 'state': 'Maharashtra'},

        # Punjab & Haryana
        {'code': 'ASR', 'name': 'Amritsar Junction', 'city': 'Amritsar', 'state': 'Punjab'},
        {'code': 'JUC', 'name': 'Jalandhar City', 'city': 'Jalandhar', 'state': 'Punjab'},
        {'code': 'LDH', 'name': 'Ludhiana Junction', 'city': 'Ludhiana', 'state': 'Punjab'},
        {'code': 'UMB', 'name': 'Ambala Cantonment', 'city': 'Ambala', 'state': 'Haryana'},
        {'code': 'CDG', 'name': 'Chandigarh', 'city': 'Chandigarh', 'state': 'Chandigarh'},
        {'code': 'PNP', 'name': 'Panipat Junction', 'city': 'Panipat', 'state': 'Haryana'},
        {'code': 'KKDE', 'name': 'Kurukshetra Junction', 'city': 'Kurukshetra', 'state': 'Haryana'},

        # Jammu & Kashmir
        {'code': 'JAT', 'name': 'Jammu Tawi', 'city': 'Jammu', 'state': 'Jammu and Kashmir'},
        {'code': 'UHP', 'name': 'Udhampur', 'city': 'Udhampur', 'state': 'Jammu and Kashmir'},
        {'code': 'SGRR', 'name': 'Srinagar', 'city': 'Srinagar', 'state': 'Jammu and Kashmir'},

        # Northeast India
        {'code': 'GHY', 'name': 'Guwahati', 'city': 'Guwahati', 'state': 'Assam'},

    for station_data in stations_data:
        Station.objects.get_or_create(
            code=station_data['code'],
            defaults=station_data
        )
    print(f"Populated {len(stations_data)} stations")

def populate_trains():
    """Populate popular Indian trains"""
    trains_data = [
        {
            'train_number': '12841',
            'train_name': 'Coromandel Express',
            'train_type': 'EXPRESS',
            'total_coaches': 24,
            'seats_per_coach': 72,
            'ac_first_seats': 24,
            'ac_two_tier_seats': 48,
            'ac_three_tier_seats': 144,
            'sleeper_seats': 576,
            'general_seats': 288,
        },
        {
            'train_number': '12627',
            'train_name': 'Karnataka Express',
            'train_type': 'EXPRESS',
            'total_coaches': 22,
            'seats_per_coach': 72,
            'ac_first_seats': 0,
            'ac_two_tier_seats': 48,
            'ac_three_tier_seats': 144,
            'sleeper_seats': 576,
            'general_seats': 288,
        },
        {
            'train_number': '12723',
            'train_name': 'Telangana Express',
            'train_type': 'EXPRESS',
            'total_coaches': 20,
            'seats_per_coach': 72,
            'ac_first_seats': 0,
            'ac_two_tier_seats': 48,
            'ac_three_tier_seats': 144,
            'sleeper_seats': 576,
            'general_seats': 288,
        },
        {
            'train_number': '12703',
            'train_name': 'Falaknuma Express',
            'train_type': 'EXPRESS',
            'total_coaches': 18,
            'seats_per_coach': 72,
            'ac_first_seats': 0,
            'ac_two_tier_seats': 48,
            'ac_three_tier_seats': 144,
            'sleeper_seats': 576,
            'general_seats': 288,
        },
        {
            'train_number': '12739',
            'train_name': 'Visakhapatnam Garib Rath',
            'train_type': 'EXPRESS',
            'total_coaches': 16,
            'seats_per_coach': 72,
            'ac_first_seats': 0,
            'ac_two_tier_seats': 0,
            'ac_three_tier_seats': 576,
            'sleeper_seats': 0,
            'general_seats': 0,
        },
        {
            'train_number': '18519',
            'train_name': 'Visakhapatnam Mumbai LTT Express',
            'train_type': 'EXPRESS',
            'total_coaches': 20,
            'seats_per_coach': 72,
            'ac_first_seats': 0,
            'ac_two_tier_seats': 48,
            'ac_three_tier_seats': 144,
            'sleeper_seats': 576,
            'general_seats': 288,
        },
        {
            'train_number': '22815',
            'train_name': 'Bilaspur Ernakulam Superfast Express',
            'train_type': 'EXPRESS',
            'total_coaches': 22,
            'seats_per_coach': 72,
            'ac_first_seats': 0,
            'ac_two_tier_seats': 48,
            'ac_three_tier_seats': 144,
            'sleeper_seats': 576,
            'general_seats': 288,
        },
        {
            'train_number': '12511',
            'train_name': 'Rapti Sagar Express',
            'train_type': 'EXPRESS',
            'total_coaches': 24,
            'seats_per_coach': 72,
            'ac_first_seats': 24,
            'ac_two_tier_seats': 48,
            'ac_three_tier_seats': 144,
            'sleeper_seats': 576,
            'general_seats': 288,
        },
        {
            'train_number': '12512',
            'train_name': 'Rapti Sagar Express',
            'train_type': 'EXPRESS',
            'total_coaches': 24,
            'seats_per_coach': 72,
            'ac_first_seats': 24,
            'ac_two_tier_seats': 48,
            'ac_three_tier_seats': 144,
            'sleeper_seats': 576,
            'general_seats': 288,
        },
        {
            'train_number': '12721',
            'train_name': 'Hyderabad Nizamabad Intercity Express',
            'train_type': 'EXPRESS',
            'total_coaches': 12,
            'seats_per_coach': 72,
            'ac_first_seats': 0,
            'ac_two_tier_seats': 0,
            'ac_three_tier_seats': 0,
            'sleeper_seats': 432,
            'general_seats': 432,
        },
    ]

    for train_data in trains_data:
        Train.objects.get_or_create(
            train_number=train_data['train_number'],
            defaults=train_data
        )
    print(f"Populated {len(trains_data)} trains")

def populate_routes():
    """Populate train routes"""
    routes_data = [
        # Coromandel Express: Chennai - Howrah
        {'train_number': '12841', 'source_code': 'MAS', 'dest_code': 'HWH', 'distance': 1659, 'duration_hours': 29, 'duration_minutes': 45, 'base_fare_per_km': 0.5},
        {'train_number': '12841', 'source_code': 'HWH', 'dest_code': 'MAS', 'distance': 1659, 'duration_hours': 29, 'duration_minutes': 45, 'base_fare_per_km': 0.5},

        # Karnataka Express: Bangalore - New Delhi
        {'train_number': '12627', 'source_code': 'SBC', 'dest_code': 'NDLS', 'distance': 2364, 'duration_hours': 40, 'duration_minutes': 30, 'base_fare_per_km': 0.45},
        {'train_number': '12627', 'source_code': 'NDLS', 'dest_code': 'SBC', 'distance': 2364, 'duration_hours': 40, 'duration_minutes': 30, 'base_fare_per_km': 0.45},

        # Telangana Express: Hyderabad - New Delhi
        {'train_number': '12723', 'source_code': 'HYB', 'dest_code': 'NDLS', 'distance': 1668, 'duration_hours': 27, 'duration_minutes': 45, 'base_fare_per_km': 0.48},
        {'train_number': '12723', 'source_code': 'NDLS', 'dest_code': 'HYB', 'distance': 1668, 'duration_hours': 27, 'duration_minutes': 45, 'base_fare_per_km': 0.48},

        # Falaknuma Express: Hyderabad - Secunderabad - Howrah
        {'train_number': '12703', 'source_code': 'HYB', 'dest_code': 'HWH', 'distance': 1468, 'duration_hours': 25, 'duration_minutes': 30, 'base_fare_per_km': 0.47},
        {'train_number': '12703', 'source_code': 'HWH', 'dest_code': 'HYB', 'distance': 1468, 'duration_hours': 25, 'duration_minutes': 30, 'base_fare_per_km': 0.47},

        # Visakhapatnam Garib Rath: Visakhapatnam - Nagpur
        {'train_number': '12739', 'source_code': 'VSKP', 'dest_code': 'NAGPUR', 'distance': 762, 'duration_hours': 14, 'duration_minutes': 15, 'base_fare_per_km': 0.4},
        {'train_number': '12739', 'source_code': 'NAGPUR', 'dest_code': 'VSKP', 'distance': 762, 'duration_hours': 14, 'duration_minutes': 15, 'base_fare_per_km': 0.4},

        # Visakhapatnam Mumbai Express
        {'train_number': '18519', 'source_code': 'VSKP', 'dest_code': 'CSTM', 'distance': 1337, 'duration_hours': 26, 'duration_minutes': 45, 'base_fare_per_km': 0.42},
        {'train_number': '18519', 'source_code': 'CSTM', 'dest_code': 'VSKP', 'distance': 1337, 'duration_hours': 26, 'duration_minutes': 45, 'base_fare_per_km': 0.42},

        # Bilaspur Ernakulam Express
        {'train_number': '22815', 'source_code': 'BILASPUR', 'dest_code': 'ERS', 'distance': 1852, 'duration_hours': 33, 'duration_minutes': 30, 'base_fare_per_km': 0.44},
        {'train_number': '22815', 'source_code': 'ERS', 'dest_code': 'BILASPUR', 'distance': 1852, 'duration_hours': 33, 'duration_minutes': 30, 'base_fare_per_km': 0.44},

        # Rapti Sagar Express: Lucknow - Jabalpur - Bilaspur - Raipur - Visakhapatnam
        {'train_number': '12511', 'source_code': 'LKO', 'dest_code': 'VSKP', 'distance': 1125, 'duration_hours': 22, 'duration_minutes': 15, 'base_fare_per_km': 0.46},
        {'train_number': '12512', 'source_code': 'VSKP', 'dest_code': 'LKO', 'distance': 1125, 'duration_hours': 22, 'duration_minutes': 15, 'base_fare_per_km': 0.46},

        # Hyderabad Nizamabad Intercity
        {'train_number': '12721', 'source_code': 'HYB', 'dest_code': 'NZB', 'distance': 167, 'duration_hours': 3, 'duration_minutes': 15, 'base_fare_per_km': 0.35},
        {'train_number': '12721', 'source_code': 'NZB', 'dest_code': 'HYB', 'distance': 167, 'duration_hours': 3, 'duration_minutes': 15, 'base_fare_per_km': 0.35},
    ]

    for route_data in routes_data:
        try:
            train = Train.objects.get(train_number=route_data['train_number'])
            source = Station.objects.get(code=route_data['source_code'])
            dest = Station.objects.get(code=route_data['dest_code'])

            Route.objects.get_or_create(
                train=train,
                source=source,
                destination=dest,
                defaults={
                    'distance': route_data['distance'],
                    'duration_hours': route_data['duration_hours'],
                    'duration_minutes': route_data['duration_minutes'],
                    'base_fare_per_km': route_data['base_fare_per_km'],
                }
            )
        except (Train.DoesNotExist, Station.DoesNotExist) as e:
            print(f"Skipping route {route_data['train_number']} {route_data['source_code']}-{route_data['dest_code']}: {e}")
    print("Populated routes")

def populate_schedules():
    """Populate train schedules"""
    schedules_data = [
        # Coromandel Express
        {'train_number': '12841', 'source_code': 'MAS', 'dest_code': 'HWH', 'departure_time': time(8, 45), 'arrival_time': time(14, 30), 'runs_on': '0123456'},
        {'train_number': '12841', 'source_code': 'HWH', 'dest_code': 'MAS', 'departure_time': time(14, 50), 'arrival_time': time(20, 35), 'runs_on': '0123456'},

        # Karnataka Express
        {'train_number': '12627', 'source_code': 'SBC', 'dest_code': 'NDLS', 'departure_time': time(19, 20), 'arrival_time': time(11, 50), 'runs_on': '0123456'},
        {'train_number': '12627', 'source_code': 'NDLS', 'dest_code': 'SBC', 'departure_time': time(17, 30), 'arrival_time': time(10, 0), 'runs_on': '0123456'},

        # Telangana Express
        {'train_number': '12723', 'source_code': 'HYB', 'dest_code': 'NDLS', 'departure_time': time(16, 50), 'arrival_time': time(20, 35), 'runs_on': '0123456'},
        {'train_number': '12723', 'source_code': 'NDLS', 'dest_code': 'HYB', 'departure_time': time(6, 25), 'arrival_time': time(10, 10), 'runs_on': '0123456'},

        # Falaknuma Express
        {'train_number': '12703', 'source_code': 'HYB', 'dest_code': 'HWH', 'departure_time': time(16, 45), 'arrival_time': time(18, 15), 'runs_on': '0123456'},
        {'train_number': '12703', 'source_code': 'HWH', 'dest_code': 'HYB', 'departure_time': time(6, 35), 'arrival_time': time(8, 5), 'runs_on': '0123456'},

        # Visakhapatnam Garib Rath
        {'train_number': '12739', 'source_code': 'VSKP', 'dest_code': 'NAGPUR', 'departure_time': time(19, 45), 'arrival_time': time(10, 0), 'runs_on': '0123456'},
        {'train_number': '12739', 'source_code': 'NAGPUR', 'dest_code': 'VSKP', 'departure_time': time(16, 0), 'arrival_time': time(6, 15), 'runs_on': '0123456'},

        # Visakhapatnam Mumbai Express
        {'train_number': '18519', 'source_code': 'VSKP', 'dest_code': 'CSTM', 'departure_time': time(12, 30), 'arrival_time': time(15, 15), 'runs_on': '0123456'},
        {'train_number': '18519', 'source_code': 'CSTM', 'dest_code': 'VSKP', 'departure_time': time(8, 5), 'arrival_time': time(10, 50), 'runs_on': '0123456'},

        # Bilaspur Ernakulam Express
        {'train_number': '22815', 'source_code': 'BILASPUR', 'dest_code': 'ERS', 'departure_time': time(5, 40), 'arrival_time': time(15, 10), 'runs_on': '0123456'},
        {'train_number': '22815', 'source_code': 'ERS', 'dest_code': 'BILASPUR', 'departure_time': time(22, 30), 'arrival_time': time(8, 0), 'runs_on': '0123456'},

        # Rapti Sagar Express
        {'train_number': '12511', 'source_code': 'LKO', 'dest_code': 'VSKP', 'departure_time': time(6, 35), 'arrival_time': time(4, 50), 'runs_on': '0123456'},
        {'train_number': '12512', 'source_code': 'VSKP', 'dest_code': 'LKO', 'departure_time': time(11, 45), 'arrival_time': time(10, 0), 'runs_on': '0123456'},

        # Hyderabad Nizamabad Intercity
        {'train_number': '12721', 'source_code': 'HYB', 'dest_code': 'NZB', 'departure_time': time(6, 0), 'arrival_time': time(9, 15), 'runs_on': '0123456'},
        {'train_number': '12721', 'source_code': 'NZB', 'dest_code': 'HYB', 'departure_time': time(17, 30), 'arrival_time': time(20, 45), 'runs_on': '0123456'},
    ]

    for schedule_data in schedules_data:
        try:
            route = Route.objects.get(
                train__train_number=schedule_data['train_number'],
                source__code=schedule_data['source_code'],
                destination__code=schedule_data['dest_code']
            )

            Schedule.objects.get_or_create(
                route=route,
                departure_time=schedule_data['departure_time'],
                defaults={
                    'arrival_time': schedule_data['arrival_time'],
                    'runs_on': schedule_data['runs_on'],
                    'ac_first_available': 24 if route.train.ac_first_seats > 0 else 0,
                    'ac_two_tier_available': 48 if route.train.ac_two_tier_seats > 0 else 0,
                    'ac_three_tier_available': 144 if route.train.ac_three_tier_seats > 0 else 0,
                    'sleeper_available': 576 if route.train.sleeper_seats > 0 else 0,
                    'general_available': 288 if route.train.general_seats > 0 else 0,
                }
            )
        except Route.DoesNotExist as e:
            print(f"Skipping schedule for {schedule_data['train_number']} {schedule_data['source_code']}-{schedule_data['dest_code']}: {e}")
    print("Populated schedules")

if __name__ == '__main__':
    print("Starting data population...")
    populate_stations()
    populate_trains()
    populate_routes()
    populate_schedules()
    print("Data population completed!")
