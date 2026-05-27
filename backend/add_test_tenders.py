import asyncio
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import select

ROOT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT_DIR))

load_dotenv(Path('..') / '.env')

from services.tender_service import db, models

async def main():
    async with db.async_session() as session:
        result = await session.execute(select(models.Tender))
        if result.scalars().first() is not None:
            print('Tender records already exist, skipping sample insert.')
            return

        now = datetime.utcnow()
        sample_tenders = [
            models.Tender(
                source='cppt',
                source_tender_id='TDR-001',
                title='Smart City Transit Analytics',
                description='Analytics platform for optimizing urban transit routes and scheduling.',
                authority='Urban Development Corporation',
                deadline=now + timedelta(days=18),
                estimated_value=5200000.0,
                category='Transportation',
                region='Karnataka',
                tender_url='https://cppt.gov.in/tenders/TDR-001',
                status='open',
                raw_metadata={'priority': 'high'},
            ),
            models.Tender(
                source='cppt',
                source_tender_id='TDR-002',
                title='Renewable Energy Microgrid Deployment',
                description='Deployment of solar microgrid systems for remote village electrification.',
                authority='Energy Ministry',
                deadline=now + timedelta(days=25),
                estimated_value=3300000.0,
                category='Energy',
                region='Tamil Nadu',
                tender_url='https://cppt.gov.in/tenders/TDR-002',
                status='open',
                raw_metadata={'renewables': True},
            ),
            models.Tender(
                source='cppt',
                source_tender_id='TDR-003',
                title='Healthcare Records Modernization',
                description='Modernize patient records systems for state healthcare providers.',
                authority='Health Services Board',
                deadline=now + timedelta(days=12),
                estimated_value=2100000.0,
                category='Healthcare',
                region='Kerala',
                tender_url='https://cppt.gov.in/tenders/TDR-003',
                status='open',
                raw_metadata={'compliance': 'HIPAA-like'},
            ),
        ]

        session.add_all(sample_tenders)
        await session.commit()

        analysis_rows = [
            models.TenderAnalysis(
                tender_id=1,
                summary='High alignment with government digital transformation goals.',
                eligibility=['Technical capacity', 'Project experience', 'Financial stability'],
                required_documents=['Company profile', 'Project portfolio', 'Bank statement'],
                risk_level='Medium',
                risk_reasons=['Tight deadline', 'High vendor competition'],
                category='Transportation',
                deadline=(now + timedelta(days=18)).strftime('%Y-%m-%d'),
                budget='₹52 Lakh',
                confidence_score=0.86,
                match_score=89.0,
                relevance_score=0.91,
                success_probability=0.78,
                raw_response={'source': 'AI analysis'},
            ),
            models.TenderAnalysis(
                tender_id=2,
                summary='Strong fit for renewable deployment vendors with microgrid experience.',
                eligibility=['Technical accreditation', 'Equipment supply chain', 'Local partner'],
                required_documents=['Equipment specs', 'Project timeline', 'Safety certifications'],
                risk_level='High',
                risk_reasons=['Logistics complexity', 'remote site access'],
                category='Energy',
                deadline=(now + timedelta(days=25)).strftime('%Y-%m-%d'),
                budget='₹33 Lakh',
                confidence_score=0.79,
                match_score=84.0,
                relevance_score=0.87,
                success_probability=0.72,
                raw_response={'source': 'AI analysis'},
            ),
            models.TenderAnalysis(
                tender_id=3,
                summary='Healthcare modernization project with low regulatory obstacles.',
                eligibility=['Data privacy compliance', 'Health IT certifications', 'Support team'],
                required_documents=['Security plan', 'Implementation roadmap', 'Training materials'],
                risk_level='Low',
                risk_reasons=['Mature provider ecosystem', 'clear requirements'],
                category='Healthcare',
                deadline=(now + timedelta(days=12)).strftime('%Y-%m-%d'),
                budget='₹21 Lakh',
                confidence_score=0.92,
                match_score=93.0,
                relevance_score=0.95,
                success_probability=0.84,
                raw_response={'source': 'AI analysis'},
            ),
        ]

        session.add_all(analysis_rows)
        await session.commit()

        risk_rows = [
            models.RiskAssessment(tender_id=1, issue='Deadline pressure', severity='Medium', detail='Resource ramp-up required immediately.'),
            models.RiskAssessment(tender_id=2, issue='Remote logistics', severity='High', detail='Site access may be interrupted during monsoon.'),
            models.RiskAssessment(tender_id=3, issue='Compliance review', severity='Low', detail='Standard healthcare security procedures required.'),
        ]
        session.add_all(risk_rows)
        await session.commit()

        notification_rows = [
            models.Notification(title='New tender available', message='Smart City Transit Analytics now live.', notification_type='new'),
            models.Notification(title='Deadline approaching', message='Healthcare Records Modernization deadline in 12 days.', notification_type='deadline'),
            models.Notification(title='Risk alert issued', message='Renewable Energy Microgrid Deployment has logistics risk.', notification_type='risk'),
        ]
        session.add_all(notification_rows)
        await session.commit()

        print('Inserted sample tender records and related analysis data.')


if __name__ == '__main__':
    asyncio.run(main())
