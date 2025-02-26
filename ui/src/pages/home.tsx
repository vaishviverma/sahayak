import { Helmet } from 'react-helmet-async';

import { CONFIG } from 'src/config-global';

import { OverviewAnalyticsView } from 'src/sections/overview/view';

// ----------------------------------------------------------------------

export default function Page() {
  return (
    <>
      <Helmet>
        <title>Sahayak Dashboard</title>
        <meta
          name="description"
          content="Sahayak is an AI-powered chatbot designed to assist grocery store owners with sales analysis, invoice processing, and customer insights."
        />
        
      </Helmet>

      <OverviewAnalyticsView />
    </>
  );
}
