import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { ConfigCard } from '../components/common/ConfigCard';
import { DashboardLayout } from '../layouts/DashboardLayout';

export const Dashboard: React.FC = () => {
    const { user } = useAuth();
    
    return (
        <DashboardLayout>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                <ConfigCard
                    title="Company Posts"
                    description="Configure company page synchronization"
                    link="/company-config"
                />
                <ConfigCard
                    title="Job Alerts"
                    description="Set up job scraping filters"
                    link="/job-config"
                />
                <ConfigCard
                    title="Trend Alerts"
                    description="Configure LinkedIn trend tracking"
                    link="/trend-config"
                />
            </div>
        </DashboardLayout>
    );
}; 