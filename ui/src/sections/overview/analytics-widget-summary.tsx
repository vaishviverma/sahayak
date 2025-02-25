import { useEffect, useState } from "react";
import axios from "axios";
import type { CardProps } from "@mui/material/Card";
import type { ColorType } from "src/theme/core/palette";
import type { ChartOptions } from "src/components/chart";

import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import { useTheme, Theme, PaletteColor } from "@mui/material/styles";
import type { Color } from "@mui/material";

import { fNumber, fPercent, fShortenNumber } from "src/utils/format-number";

import { varAlpha, bgGradient } from "src/theme/styles";

import { Iconify } from "src/components/iconify";
import { SvgColor } from "src/components/svg-color";
import { Chart, useChart } from "src/components/chart";

// ----------------------------------------------------------------------

type Props = CardProps & {
  title: string;
  apiUrl: string; 
  color?: keyof Theme["palette"];
  icon: React.ReactNode;
};

export function AnalyticsWidgetSummary({ title, apiUrl, icon, color = "primary", sx, ...other }: Props) {
  const theme = useTheme() as Theme;


  const [data, setData] = useState({
    total: 0,
    percent: 0,
    categories: [],
    series: [],
  });

  useEffect(() => {
    const fetchGrossIncome = async () => {
      try {
        const response = await axios.get(apiUrl); // Use the provided API URL
        const resData = response.data;

        setData({
          total: resData.first,
          categories: resData.second,
          series: resData.third,
          percent: resData.fourth || 0, // Default to 0 if not provided
        });
      } catch (error) {
        console.error(`Error fetching data from ${apiUrl}:`, error);
      }
    };

    fetchGrossIncome();
  }, [apiUrl]);

  const chartColors = [
    (theme.palette[color as keyof Theme["palette"]] as PaletteColor)?.dark ||
      theme.palette.primary.dark,
  ];
  

  const chartOptions = useChart({
    chart: { sparkline: { enabled: true } },
    colors: chartColors,
    xaxis: { categories: data.categories },
    grid: {
      padding: { top: 6, left: 6, right: 6, bottom: 6 },
    },
    tooltip: {
      y: { formatter: (value: number) => fNumber(value), title: { formatter: () => "" } },
    },
  });
  const lightChannel =
              (theme.vars.palette[color as keyof typeof theme.vars.palette] as
                | { lightChannel: string }
                | undefined)?.lightChannel || theme.vars.palette.primary.lightChannel;

            const mainChannel =
              (theme.vars.palette[color as keyof typeof theme.vars.palette] as
                | { mainChannel: string }
                | undefined)?.mainChannel || theme.vars.palette.primary.mainChannel;
  const renderTrending = (
    <Box
      sx={{
        top: 16,
        gap: 0.5,
        right: 16,
        display: "flex",
        position: "absolute",
        alignItems: "center",
      }}
    >
      <Iconify width={20} icon={data.percent < 0 ? "eva:trending-down-fill" : "eva:trending-up-fill"} />
      <Box component="span" sx={{ typography: "subtitle2" }}>
        {data.percent > 0 && "+"}
        {fPercent(data.percent)}
      </Box>
    </Box>
  );

  return (
    <Card
      sx={{
        ...bgGradient({

            color: `135deg, ${varAlpha(lightChannel, 0.48)}, ${varAlpha(mainChannel, 0.48)}`,

        }),
        p: 3,
        boxShadow: "none",
        position: "relative",
        color: `${color}.darker`,
        backgroundColor: "common.white",
        ...sx,
      }}
      {...other}
    >
      <Box sx={{ width: 48, height: 48, mb: 3 }}>{icon}</Box>

      {renderTrending}

      <Box
        sx={{
          display: "flex",
          flexWrap: "wrap",
          alignItems: "flex-end",
          justifyContent: "flex-end",
        }}
      >
        <Box sx={{ flexGrow: 1, minWidth: 112 }}>
          <Box sx={{ mb: 1, typography: "subtitle2" }}>{title}</Box>
          <Box sx={{ typography: "h4" }}>{fShortenNumber(data.total)}</Box>
        </Box>

        <Chart type="line" series={[{ data: data.series }]} options={chartOptions} width={84} height={56} />
      </Box>

      <SvgColor
        src="/assets/background/shape-square.svg"
        sx={{
          top: 0,
          left: -20,
          width: 240,
          zIndex: -1,
          height: 240,
          opacity: 0.24,
          position: "absolute",
          color: (theme.palette[color as keyof Theme["palette"]] as PaletteColor)?.main || theme.palette.primary.main,

        }}
      />
    </Card>
  );
}
