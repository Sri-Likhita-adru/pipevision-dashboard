from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import random
import json

app = Flask(__name__)

# PACP defect code mappings (compliant with PACP 7.0)
PACP_CODES = {
    'corrosion': [
        {'code': 'COR-1', 'name': 'Light Corrosion', 'score': 1, 'description': 'Surface oxidation visible'},
        {'code': 'COR-2', 'name': 'Moderate Corrosion', 'score': 2, 'description': 'Material thinning <10%'},
        {'code': 'COR-3', 'name': 'Medium Corrosion', 'score': 3, 'description': 'Material thinning 10-30%'},
        {'code': 'COR-4', 'name': 'Severe Corrosion', 'score': 4, 'description': 'Material thinning 30-50%'},
        {'code': 'COR-5', 'name': 'Critical Corrosion', 'score': 5, 'description': 'Material thinning >50%'},
    ],
    'crack': [
        {'code': 'CL-1', 'name': 'Hairline Longitudinal Crack', 'score': 1, 'description': 'Width <1mm'},
        {'code': 'CL-2', 'name': 'Minor Longitudinal Crack', 'score': 2, 'description': 'Width 1-3mm'},
        {'code': 'CL-3', 'name': 'Medium Longitudinal Crack', 'score': 3, 'description': 'Width 3-10mm'},
        {'code': 'CL-4', 'name': 'Severe Longitudinal Crack', 'score': 4, 'description': 'Width >10mm'},
        {'code': 'CL-5', 'name': 'Critical Longitudinal Crack', 'score': 5, 'description': 'Structural failure'},
        {'code': 'CR-1', 'name': 'Hairline Circumferential Crack', 'score': 1, 'description': 'Width <1mm'},
        {'code': 'CR-2', 'name': 'Minor Circumferential Crack', 'score': 2, 'description': 'Width 1-3mm'},
        {'code': 'CR-3', 'name': 'Medium Circumferential Crack', 'score': 3, 'description': 'Width 3-10mm'},
        {'code': 'FR-4', 'name': 'Severe Fracture', 'score': 4, 'description': 'Pipe segments separated'},
        {'code': 'FR-5', 'name': 'Critical Fracture', 'score': 5, 'description': 'Complete structural failure'},
    ],
    'deposit': [
        {'code': 'DEP-1', 'name': 'Light Deposits', 'score': 1, 'description': 'Coverage <20%'},
        {'code': 'DEP-2', 'name': 'Moderate Deposits', 'score': 2, 'description': 'Coverage 20-50%'},
        {'code': 'DEP-3', 'name': 'Heavy Deposits', 'score': 3, 'description': 'Coverage >50%'},
    ],
    'root': [
        {'code': 'RO-1', 'name': 'Fine Roots', 'score': 1, 'description': 'Fine root hairs'},
        {'code': 'RO-2', 'name': 'Tap Root', 'score': 2, 'description': 'Single root penetration'},
        {'code': 'RO-3', 'name': 'Medium Root Mass', 'score': 3, 'description': 'Multiple roots, flow restricted'},
        {'code': 'RO-4', 'name': 'Severe Root Intrusion', 'score': 4, 'description': 'Heavy root mass, blockage'},
    ],
    'deformation': [
        {'code': 'DEF-1', 'name': 'Minor Deformation', 'score': 1, 'description': '<5% diameter change'},
        {'code': 'DEF-2', 'name': 'Moderate Deformation', 'score': 2, 'description': '5-10% diameter change'},
        {'code': 'DEF-3', 'name': 'Severe Deformation', 'score': 3, 'description': '>10% diameter change'},
    ]
}

DEFECT_CATEGORIES = ['corrosion', 'crack', 'deposit', 'root', 'deformation']

def get_random_pacp_code(severity='random'):
    """Get a random PACP code based on severity"""
    if severity == 'random':
        category = random.choice(DEFECT_CATEGORIES)
        return random.choice(PACP_CODES[category])
    elif severity == 'critical':
        # Get codes with score 4-5
        high_severity_codes = []
        for category in DEFECT_CATEGORIES:
            high_severity_codes.extend([c for c in PACP_CODES[category] if c['score'] >= 4])
        return random.choice(high_severity_codes)
    elif severity == 'high':
        # Get codes with score 3-4
        med_severity_codes = []
        for category in DEFECT_CATEGORIES:
            med_severity_codes.extend([c for c in PACP_CODES[category] if 3 <= c['score'] <= 4])
        return random.choice(med_severity_codes)
    else:
        # Get codes with score 1-2
        low_severity_codes = []
        for category in DEFECT_CATEGORIES:
            low_severity_codes.extend([c for c in PACP_CODES[category] if c['score'] <= 2])
        return random.choice(low_severity_codes)

# Mock data generators
def generate_pipe_segments():
    """Generate 14 pipe segments: 4 Poor, 2 Fair, 6 Good, 2 Great"""
    pipe_types = ['PVC', 'Concrete', 'Clay', 'HDPE']
    
    segments = [
        # Critical/Poor (4 segments)
        {'id': 'pipe-1', 'name': 'A-004', 'quality': 'Poor', 'pipeType': 'Concrete', 'diameter': 300, 'lengthMeters': 145, 'estimatedAge': 51, 'durabilityScore': 21, 'latitude': 42.2808, 'longitude': -83.7430, 'lastInspectionDate': (datetime.now() - timedelta(days=45)).isoformat()},
        {'id': 'pipe-2', 'name': 'A-007', 'quality': 'Poor', 'pipeType': 'Concrete', 'diameter': 250, 'lengthMeters': 198, 'estimatedAge': 47, 'durabilityScore': 23, 'latitude': 42.2815, 'longitude': -83.7445, 'lastInspectionDate': (datetime.now() - timedelta(days=38)).isoformat()},
        {'id': 'pipe-3', 'name': 'A-009', 'quality': 'Poor', 'pipeType': 'Clay', 'diameter': 200, 'lengthMeters': 176, 'estimatedAge': 55, 'durabilityScore': 18, 'latitude': 42.2822, 'longitude': -83.7460, 'lastInspectionDate': (datetime.now() - timedelta(days=52)).isoformat()},
        {'id': 'pipe-4', 'name': 'B-003', 'quality': 'Poor', 'pipeType': 'Concrete', 'diameter': 300, 'lengthMeters': 203, 'estimatedAge': 49, 'durabilityScore': 22, 'latitude': 42.2795, 'longitude': -83.7415, 'lastInspectionDate': (datetime.now() - timedelta(days=41)).isoformat()},
        
        # High Risk/Fair (2 segments)
        {'id': 'pipe-5', 'name': 'A-012', 'quality': 'Fair', 'pipeType': 'PVC', 'diameter': 150, 'lengthMeters': 156, 'estimatedAge': 28, 'durabilityScore': 68, 'latitude': 42.2829, 'longitude': -83.7475, 'lastInspectionDate': (datetime.now() - timedelta(days=90)).isoformat()},
        {'id': 'pipe-6', 'name': 'B-008', 'quality': 'Fair', 'pipeType': 'Concrete', 'diameter': 250, 'lengthMeters': 187, 'estimatedAge': 32, 'durabilityScore': 62, 'latitude': 42.2788, 'longitude': -83.7400, 'lastInspectionDate': (datetime.now() - timedelta(days=85)).isoformat()},
        
        # Good (6 segments)
        {'id': 'pipe-7', 'name': 'A-015', 'quality': 'Good', 'pipeType': 'PVC', 'diameter': 200, 'lengthMeters': 234, 'estimatedAge': 15, 'durabilityScore': 85, 'latitude': 42.2836, 'longitude': -83.7490, 'lastInspectionDate': (datetime.now() - timedelta(days=120)).isoformat()},
        {'id': 'pipe-8', 'name': 'C-001', 'quality': 'Good', 'pipeType': 'PVC', 'diameter': 150, 'lengthMeters': 167, 'estimatedAge': 18, 'durabilityScore': 82, 'latitude': 42.2780, 'longitude': -83.7480, 'lastInspectionDate': (datetime.now() - timedelta(days=115)).isoformat()},
        {'id': 'pipe-9', 'name': 'C-005', 'quality': 'Good', 'pipeType': 'HDPE', 'diameter': 200, 'lengthMeters': 198, 'estimatedAge': 12, 'durabilityScore': 89, 'latitude': 42.2773, 'longitude': -83.7465, 'lastInspectionDate': (datetime.now() - timedelta(days=130)).isoformat()},
        {'id': 'pipe-10', 'name': 'D-002', 'quality': 'Good', 'pipeType': 'PVC', 'diameter': 150, 'lengthMeters': 145, 'estimatedAge': 16, 'durabilityScore': 84, 'latitude': 42.2843, 'longitude': -83.7505, 'lastInspectionDate': (datetime.now() - timedelta(days=125)).isoformat()},
        {'id': 'pipe-11', 'name': 'D-006', 'quality': 'Good', 'pipeType': 'HDPE', 'diameter': 200, 'lengthMeters': 189, 'estimatedAge': 14, 'durabilityScore': 87, 'latitude': 42.2766, 'longitude': -83.7450, 'lastInspectionDate': (datetime.now() - timedelta(days=128)).isoformat()},
        {'id': 'pipe-12', 'name': 'E-003', 'quality': 'Good', 'pipeType': 'PVC', 'diameter': 150, 'lengthMeters': 156, 'estimatedAge': 17, 'durabilityScore': 83, 'latitude': 42.2850, 'longitude': -83.7520, 'lastInspectionDate': (datetime.now() - timedelta(days=118)).isoformat()},
        
        # Great (2 segments)
        {'id': 'pipe-13', 'name': 'E-007', 'quality': 'Great', 'pipeType': 'HDPE', 'diameter': 200, 'lengthMeters': 212, 'estimatedAge': 5, 'durabilityScore': 95, 'latitude': 42.2759, 'longitude': -83.7435, 'lastInspectionDate': (datetime.now() - timedelta(days=180)).isoformat()},
        {'id': 'pipe-14', 'name': 'F-001', 'quality': 'Great', 'pipeType': 'HDPE', 'diameter': 150, 'lengthMeters': 178, 'estimatedAge': 7, 'durabilityScore': 93, 'latitude': 42.2857, 'longitude': -83.7535, 'lastInspectionDate': (datetime.now() - timedelta(days=175)).isoformat()}
    ]
    
    return segments

def generate_sensor_readings(pipe_segments):
    readings = []
    for i in range(100):
        pipe = random.choice(pipe_segments)
        
        # Generate PACP observation based on sensor data
        pacp_code = get_random_pacp_code('random')
        
        # Calculate risk score based on PACP score
        risk_score = round((pacp_code['score'] / 5) * 10, 1)
        
        reading = {
            'id': f'reading-{i+1}',
            'pipeSegmentId': pipe['id'],
            'pipeSegmentName': pipe['name'],
            'timestamp': (datetime.now() - timedelta(hours=random.randint(0, 72))).isoformat(),
            'temperature': round(20 + random.uniform(-5, 10), 1),
            'soundLevel': round(45 + random.uniform(-10, 25), 1),
            'flowRate': round(random.uniform(5, 20), 2),
            'cameraImageUrl': f'/static/images/camera-{random.randint(1, 5)}.jpg' if random.random() > 0.3 else None,
            # PACP fields
            'pacp_code': pacp_code['code'],
            'pacp_name': pacp_code['name'],
            'pacp_score': pacp_code['score'],
            'observation': pacp_code['description'],
            'risk_score': risk_score
        }
        readings.append(reading)
    
    return sorted(readings, key=lambda x: x['timestamp'], reverse=True)

def generate_ai_analysis(pipe_segments):
    corrosion_levels = ['None', 'Low', 'Medium', 'High', 'Critical']
    priorities = ['Low', 'Medium', 'High', 'Critical']
    soil_contaminants = ['Heavy Metals', 'Industrial Waste', 'Organic Matter', 'Chemical Residue']
    
    analyses = []
    
    # Generate AI analysis for Fair and Poor quality pipes
    for pipe in pipe_segments:
        if pipe['quality'] in ['Fair', 'Poor']:
            corrosion_level = random.choice(corrosion_levels[2:]) if pipe['quality'] == 'Poor' else random.choice(corrosion_levels[1:3])
            priority = 'Critical' if pipe['quality'] == 'Poor' else random.choice(priorities[1:3])
            
            # Get appropriate PACP code based on severity
            if priority == 'Critical':
                pacp_code = get_random_pacp_code('critical')
            elif priority == 'High':
                pacp_code = get_random_pacp_code('high')
            else:
                pacp_code = get_random_pacp_code('low')
            
            # Generate confidence score (higher for more severe issues)
            base_confidence = 0.75 if priority == 'Critical' else 0.70
            confidence = round(base_confidence + random.uniform(0, 0.20), 4)
            
            analysis = {
                'id': f'analysis-{pipe["id"]}',
                'pipeSegmentId': pipe['id'],
                'pipeSegmentName': pipe['name'],
                'corrosionLevel': corrosion_level,
                'corrosionConfidence': confidence,
                'maintenancePriority': priority,
                'estimatedFinancialAge': pipe['estimatedAge'] + random.randint(5, 15),
                'predictedFailureMonths': random.randint(4, 48) if pipe['quality'] == 'Poor' else random.randint(12, 60),
                'soilContaminationDetected': random.sample(soil_contaminants, random.randint(1, 3)) if random.random() > 0.5 else [],
                'recommendations': f"Schedule {'immediate' if priority == 'Critical' else 'priority'} inspection and repair",
                # PACP fields
                'pacp_code': pacp_code['code'],
                'pacp_name': pacp_code['name'],
                'pacp_score': pacp_code['score'],
                'pacp_description': pacp_code['description'],
                'defect_location_meters': round(random.uniform(5, pipe['lengthMeters'] - 5), 1),
                'confidence_level': 'high' if confidence > 0.85 else 'medium' if confidence > 0.70 else 'low'
            }
            analyses.append(analysis)
    
    # Sort by priority
    priority_order = {'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1}
    return sorted(analyses, key=lambda x: priority_order[x['maintenancePriority']], reverse=True)

def generate_alerts(pipe_segments, ai_analyses):
    alerts = []
    alert_id = 1
    
    for analysis in ai_analyses:
        if analysis['maintenancePriority'] in ['Critical', 'High']:
            severity = 'critical' if analysis['maintenancePriority'] == 'Critical' else 'high'
            
            # Create detailed message with PACP code
            pacp_info = f"PACP {analysis['pacp_code']}"
            message = f"{analysis['pacp_name']} detected. {pacp_info}. Immediate action required. Predicted failure in {analysis['predictedFailureMonths']} months."
            
            alert = {
                'id': f'alert-{alert_id}',
                'pipeSegmentId': analysis['pipeSegmentId'],
                'pipeSegmentName': analysis['pipeSegmentName'],
                'severity': severity,
                'message': message,
                'timestamp': (datetime.now() - timedelta(hours=random.randint(1, 48))).isoformat(),
                # PACP fields
                'pacp_code': analysis['pacp_code'],
                'pacp_score': analysis['pacp_score'],
                'confidence': analysis['corrosionConfidence']
            }
            alerts.append(alert)
            alert_id += 1
    
    return sorted(alerts, key=lambda x: (x['severity'] == 'critical', x['timestamp']), reverse=True)

# Initialize data
pipe_segments = generate_pipe_segments()
sensor_readings = generate_sensor_readings(pipe_segments)
ai_analyses = generate_ai_analysis(pipe_segments)
alerts = generate_alerts(pipe_segments, ai_analyses)

# Routes
@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/map')
def map_view():
    return render_template('map.html')

@app.route('/raw-data')
def raw_data():
    return render_template('raw-data.html')

@app.route('/ai-analysis')
def ai_analysis_view():
    return render_template('ai-analysis.html')

# API endpoints
@app.route('/api/pipe-segments')
def get_pipe_segments():
    return jsonify(pipe_segments)

@app.route('/api/sensor-readings')
def get_sensor_readings():
    return jsonify(sensor_readings)

@app.route('/api/ai-analysis')
def get_ai_analysis():
    return jsonify(ai_analyses)

@app.route('/api/alerts')
def get_alerts():
    return jsonify(alerts)

@app.route('/api/metrics')
def get_metrics():
    pipe_segments = generate_pipe_segments()
    total_length = sum(p['lengthMeters'] for p in pipe_segments)
    avg_age = round(sum(p['estimatedAge'] for p in pipe_segments) / len(pipe_segments), 1)
    
    # Fixed quality counts: 4 Poor, 2 Fair, 6 Good, 2 Great
    quality_counts = {
        'Great': 2,
        'Good': 6,
        'Fair': 2,
        'Poor': 4
    }
    
    # Pipe type breakdown
    pipe_type_counts = {}
    for p in pipe_segments:
        pipe_type = p['pipeType']
        pipe_type_counts[pipe_type] = pipe_type_counts.get(pipe_type, 0) + 1
    
    high_risk_count = 4  # Poor segments
    
    # Calculate average quality
    avg_quality = 'Good'  # With 6 Good segments, average is Good
    
    return jsonify({
        'totalPipeLength': total_length,
        'averageAge': avg_age,
        'averageQuality': avg_quality,
        'qualityDistribution': quality_counts,
        'qualityBreakdown': {
            'great': 2,
            'good': 6,
            'fair': 2,
            'poor': 4
        },
        'pipeTypeBreakdown': pipe_type_counts,
        'highRiskSegments': high_risk_count
    })

@app.route('/api/recent-activity')
def get_recent_activity():
    activity_types = ['inspection', 'maintenance', 'alert', 'analysis']
    activities = [
        {
            'id': f'activity-{i}',
            'activityType': random.choice(activity_types),
            'description': f'Inspection completed on {random.choice(pipe_segments)["name"]}',
            'timestamp': (datetime.now() - timedelta(hours=random.randint(1, 120))).isoformat()
        }
        for i in range(5)
    ]
    
    return jsonify(sorted(activities, key=lambda x: x['timestamp'], reverse=True))

@app.route('/api/pacp-codes')
def get_pacp_codes():
    """Return all PACP codes for reference"""
    return jsonify(PACP_CODES)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)