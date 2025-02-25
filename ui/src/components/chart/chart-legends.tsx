
import Stack from '@mui/material/Stack';
import { styled } from '@mui/material/styles';
import type { BoxProps } from '@mui/material/Box';
import Box from '@mui/material/Box';
// ----------------------------------------------------------------------

export const StyledLegend = styled(Box)(({ theme }) => ({
  gap: 6,
  alignItems: 'center',
  display: 'inline-flex',
  justifyContent: 'flex-start',
  fontSize: theme.typography.pxToRem(13),
  fontWeight: theme.typography.fontWeightMedium,
}));

export const StyledDot = styled(Box)(() => ({
  width: 12,
  height: 12,
  flexShrink: 0,
  display: 'flex',
  borderRadius: '50%',
  position: 'relative',
  alignItems: 'center',
  justifyContent: 'center',
  backgroundColor: 'currentColor',
}));

// ----------------------------------------------------------------------

type Props = BoxProps & {
  labels?: string[];
  colors?: string[];
  values?: string[];
  sublabels?: string[];
  icons?: React.ReactNode[];
};

export function ChartLegends({
  icons = [],  // Ensure default empty array
  values = [],
  sublabels = [],
  labels = [],
  colors = [],
  ...other
}: Props) {
  return (
    <Box gap={2} display="flex" flexWrap="wrap" {...other}>
      {labels.map((series, index) => (
        <Stack key={`${series}-${index}`} spacing={1}>
          <StyledLegend>
            {icons.length > index ? (
              <Box
                component="span"
                sx={{ color: colors[index] || 'inherit', '& svg, & img': { width: 20, height: 20 } }}
              >
                {icons[index]}
              </Box>
            ) : (
              <StyledDot component="span" sx={{ color: colors[index] || 'inherit' }} />
            )}

            <Box component="span" sx={{ flexShrink: 0 }}>
              {series}
              {sublabels.length > index && <> {` (${sublabels[index]})`}</>}
            </Box>
          </StyledLegend>

          {values.length > index && <Box sx={{ typography: 'h6' }}>{values[index]}</Box>}
        </Stack>
      ))}
    </Box>
  );
}
