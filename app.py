from flask import Flask, render_template, jsonify
from datetime import datetime, timedelta
import random
import json

app = Flask(__name__)

# Mock data generators
def generate_pipe_segments():
    qualities = ['Great', 'Good', 'Fair', 'Poor']
    pipe_types = ['PVC', 'Concrete', 'Clay', 'Steel']
    
    segments = []
    for i in range(1, 21):
        quality = random.choice(qualities)
        segments.append({
            'id': f'pipe-{i}',
            'name': f'Segment {chr(65 + (i-1)//26)}-{str(i).zfill(3)}',
            'quality': quality,
            'pipeType': random.choice(pipe_types),
            'lengthMeters': random.randint(50, 500),
            'diameter': random.choice([150, 200, 250, 300, 400]),
            'estimatedAge': random.randint(5, 45),
            'durabilityScore': random.randint(40, 95),
            'latitude': 42.2808 + random.uniform(-0.01, 0.01),
            'longitude': -83.7430 + random.uniform(-0.01, 0.01),
            'lastInspectionDate': (datetime.now() - timedelta(days=random.randint(1, 365))).isoformat()
        })
    
    return segments

def generate_sensor_readings(pipe_segments):
    readings = []
    for i in range(100):
        pipe = random.choice(pipe_segments)
        readings.append({
            'id': f'reading-{i+1}',
            'pipeSegmentId': pipe['id'],
            'timestamp': (datetime.now() - timedelta(hours=random.randint(0, 72))).isoformat(),
            'temperature': round(20 + random.uniform(-5, 10), 1),
            'soundLevel': round(45 + random.uniform(-10, 25), 1),
            'flowRate': round(random.uniform(5, 20), 2),
            'cameraImageUrl': f'/static/images/camera-{random.randint(1, 5)}.jpg' if random.random() > 0.3 else None
        })
    
    return sorted(readings, key=lambda x: x['timestamp'], reverse=True)

def generate_ai_analysis(pipe_segments):
    corrosion_levels = ['None', 'Low', 'Medium', 'High', 'Critical']
    priorities = ['Low', 'Medium', 'High', 'Critical']
    contaminants = ['Heavy Metals', 'Industrial Waste', 'Organic Matter', 'Chemical Residue']
    recommendations = [
        'Schedule immediate visual inspection',
        'Plan replacement within 6 months',
        'Increase monitoring frequency',
        'Apply protective coating',
        'Conduct structural integrity test'
    ]
    
    analyses = []
    for pipe in pipe_segments:
        if pipe['quality'] in ['Fair', 'Poor']:
            corrosion = 'Critical' if pipe['quality'] == 'Poor' else random.choice(['Medium', 'High'])
            priority = 'Critical' if pipe['quality'] == 'Poor' else random.choice(['Medium', 'High'])
            
            analyses.append({
                'id': f'analysis-{pipe["id"]}',
                'pipeSegmentId': pipe['id'],
                'corrosionLevel': corrosion,
                'corrosionConfidence': round(random.uniform(75, 95), 1),
                'maintenancePriority': priority,
                'estimatedFinancialAge': pipe['estimatedAge'] + random.randint(-5, 10),
                'predictedFailureMonths': random.randint(4, 24) if pipe['quality'] == 'Poor' else random.randint(12, 48),
                'soilContaminationDetected': random.sample(contaminants, random.randint(0, 2)),
                'recommendations': random.sample(recommendations, random.randint(1, 3))
            })
    
    return analyses

def generate_alerts(pipe_segments, ai_analysis):
    severities = ['critical', 'high', 'medium', 'low']
    alerts = []
    
    critical_pipes = [p for p in pipe_segments if p['quality'] == 'Poor']
    
    for i, pipe in enumerate(critical_pipes[:8]):
        analysis = next((a for a in ai_analysis if a['pipeSegmentId'] == pipe['id']), None)
        
        if i < 4:
            severity = 'critical'
            message = f"Critical corrosion detected. Immediate action required. Predicted failure in {analysis['predictedFailureMonths']} months."
        else:
            severity = 'high'
            message = f"High corrosion levels detected. Schedule inspection within 30 days."
        
        alerts.append({
            'id': f'alert-{i+1}',
            'pipeSegmentId': pipe['id'],
            'pipeSegmentName': pipe['name'],
            'severity': severity,
            'message': message,
            'timestamp': (datetime.now() - timedelta(hours=random.randint(1, 48))).isoformat()
        })
    
    return sorted(alerts, key=lambda x: {'critical': 4, 'high': 3, 'medium': 2, 'low': 1}[x['severity']], reverse=True)

def generate_system_metrics(pipe_segments):
    quality_counts = {'great': 0, 'good': 0, 'fair': 0, 'poor': 0}
    type_counts = {}
    total_length = 0
    total_age = 0
    
    for pipe in pipe_segments:
        quality_counts[pipe['quality'].lower()] += 1
        type_counts[pipe['pipeType']] = type_counts.get(pipe['pipeType'], 0) + 1
        total_length += pipe['lengthMeters']
        total_age += pipe['estimatedAge']
    
    return {
        'totalPipeLength': total_length,
        'averageAge': round(total_age / len(pipe_segments), 1),
        'averageQuality': max(quality_counts, key=quality_counts.get).capitalize(),
        'highRiskSegments': quality_counts['poor'],
        'qualityBreakdown': quality_counts,
        'pipeTypeBreakdown': type_counts
    }

def generate_recent_activity(pipe_segments):
    activity_types = ['inspection', 'analysis', 'alert', 'maintenance']
    descriptions = {
        'inspection': 'Visual inspection completed',
        'analysis': 'AI analysis completed with high confidence',
        'alert': 'Critical alert generated for high-risk segment',
        'maintenance': 'Scheduled maintenance completed'
    }
    
    activities = []
    for i in range(10):
        pipe = random.choice(pipe_segments)
        activity_type = random.choice(activity_types)
        
        activities.append({
            'id': f'activity-{i+1}',
            'pipeSegmentId': pipe['id'],
            'activityType': activity_type,
            'description': f"{descriptions[activity_type]} - {pipe['name']}",
            'timestamp': (datetime.now() - timedelta(hours=random.randint(1, 168))).isoformat()
        })
    
    return sorted(activities, key=lambda x: x['timestamp'], reverse=True)

# Generate all data
pipe_segments = generate_pipe_segments()
sensor_readings = generate_sensor_readings(pipe_segments)
ai_analysis = generate_ai_analysis(pipe_segments)
alerts = generate_alerts(pipe_segments, ai_analysis)
system_metrics = generate_system_metrics(pipe_segments)
recent_activity = generate_recent_activity(pipe_segments)

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

@app.route('/alerts')
def alerts_view():
    return render_template('alerts.html')

# API Routes
@app.route('/api/pipe-segments')
def api_pipe_segments():
    return jsonify(pipe_segments)

@app.route('/api/sensor-readings')
def api_sensor_readings():
    return jsonify(sensor_readings)

@app.route('/api/ai-analysis')
def api_ai_analysis():
    return jsonify(ai_analysis)

@app.route('/api/alerts')
def api_alerts():
    return jsonify(alerts)

@app.route('/api/metrics')
def api_metrics():
    return jsonify(system_metrics)

@app.route('/api/recent-activity')
def api_recent_activity():
    return jsonify(recent_activity)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)