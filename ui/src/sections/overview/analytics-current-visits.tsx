import { useState, useEffect } from "react"; // React Hooks

import type { CardProps } from '@mui/material/Card';
import type { ChartOptions } from 'src/components/chart';

import Card from '@mui/material/Card';
import Divider from '@mui/material/Divider';
import { useTheme } from '@mui/material/styles';
import CardHeader from '@mui/material/CardHeader';

import { fNumber } from 'src/utils/format-number';

import { Chart, useChart, ChartLegends } from 'src/components/chart';

// ----------------------------------------------------------------------

type Props = CardProps & {
  title?: string;
  subheader?: string;
  apiEndpoint: string; // Local API endpoint for fetching data
};


export function Distribution({ title, subheader, apiEndpoint, ...other }: Props) {
  const theme = useTheme();
  const [chartData, setChartData] = useState<{ label: string; value: number }[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchChartData = async () => {
      try {
        const response = await fetch(apiEndpoint);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const data = await response.json();
        if (data?.series) {
          setChartData(data.series);
        } else {
          throw new Error('Invalid API response format');
        } // Assuming API returns { series: [{ label, value }] }
      } catch (err) {
        setError((err as Error).message);
        console.error('Error fetching chart data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchChartData();
  }, [apiEndpoint]);

  const chartSeries = Array.isArray(chartData) ? chartData.map((item) => item.value) : [];
  const chartLabels = Array.isArray(chartData) ? chartData.map((item) => item.label) : [];

  const chartColors = [
    theme.palette.primary.main,
    theme.palette.warning.main,
    theme.palette.secondary.dark,
    theme.palette.error.main,
  ];

  const chartOptions = useChart({
    chart: { sparkline: { enabled: true } },
    colors: chartColors,
    labels: chartLabels,
    stroke: { width: 0 },
    dataLabels: { enabled: true, dropShadow: { enabled: false } },
    tooltip: {
      y: {
        formatter: (value: number) => fNumber(value),
        title: { formatter: (seriesName: string) => `${seriesName}` },
      },
    },
    plotOptions: { pie: { donut: { labels: { show: false } } } },
  });

  return (
    <Card {...other}>
      <CardHeader title={title} subheader={subheader} />

      {loading ? (
        <p>Loading chart...</p>
      ) : (
        <>
          <Chart
            type="pie"
            series={chartSeries}
            options={chartOptions}
            width={{ xs: 240, xl: 260 }}
            height={{ xs: 240, xl: 260 }}
            sx={{ my: 6, mx: 'auto' }}
          />

          <Divider sx={{ borderStyle: 'dashed' }} />

          <ChartLegends
            labels={chartLabels}
            colors={chartColors}
            sx={{ p: 3, justifyContent: 'center' }}
          />
        </>
      )}
    </Card>
  );
}