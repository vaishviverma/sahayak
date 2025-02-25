import Grid from '@mui/material/Unstable_Grid2';
import Typography from '@mui/material/Typography';

import { DashboardContent } from 'src/layouts/dashboard';

import { Distribution } from '../analytics-current-visits';
import { AnalyticsWidgetSummary } from '../analytics-widget-summary';
import { Chatbot } from '../chatbot';

// ----------------------------------------------------------------------

export function OverviewAnalyticsView() {
  return (
    <DashboardContent maxWidth="xl">
      <Typography variant="h4" sx={{ mb: { xs: 3, md: 5 } }}>
        Hi, Welcome Back!
      </Typography>

      <Grid container spacing={3}>
        <Grid xs={12} sm={6} md={3}>
        <AnalyticsWidgetSummary 
          title="Weekly Gross Income" 
          apiUrl="http://localhost:8000/gross-income"
          color="primary"
          icon={<img alt="icon" src="/assets/icons/glass/ic-glass-bag.svg" />}
        />
        </Grid>

        <Grid xs={12} sm={6} md={3}>
          <AnalyticsWidgetSummary
            title="Peak Hour" 
            apiUrl="http://localhost:8000/peak-hour"
            color="error"
            icon={<img alt="icon" src="/assets/icons/glass/ic-glass-bag.svg" />}
          />
        </Grid>

        <Grid xs={12} sm={6} md={3}>
          <AnalyticsWidgetSummary
            title="Weekly Total Sales" 
            apiUrl="http://localhost:8000/total-sales"
            color="success"
            icon={<img alt="icon" src="/assets/icons/glass/ic-glass-bag.svg" />}
          />
        </Grid>

        <Grid xs={12} sm={6} md={3}>
          <AnalyticsWidgetSummary
            title="Weekly Transactions" 
            apiUrl="http://localhost:8000/weekly-transactions"
            color="secondary"
            icon={<img alt="icon" src="/assets/icons/glass/ic-glass-bag.svg" />}
          />
        </Grid>

        <Grid xs={12} md={6} lg={4}>
          
          <Distribution
            title="Distribution of Products"
            subheader="Today’s data" apiEndpoint="http://localhost:8000/productdis"
          />
        </Grid>

        <Grid xs={12} md={6} lg={8}>
          <Chatbot/>
        </Grid>

{/* 
        <Grid xs={12} md={6} lg={4}>
          <AnalyticsOrderTimeline title="Order timeline" list={_timeline} />
        </Grid> */}

      </Grid>
    </DashboardContent>
  );
}
