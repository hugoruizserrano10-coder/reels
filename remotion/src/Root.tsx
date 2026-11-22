import React from 'react';
import {Composition} from 'remotion';
import {ReelPro, ReelProps} from './ReelPro';

const vacio: ReelProps = {scenes: [], words: [], voice: null, music: null, totalFrames: 90, brand: 'norte.local'};

export const Root: React.FC = () => (
  <Composition
    id="ReelPro"
    component={ReelPro as unknown as React.FC<Record<string, unknown>>}
    width={1080}
    height={1920}
    fps={30}
    durationInFrames={90}
    defaultProps={vacio as unknown as Record<string, unknown>}
    calculateMetadata={({props}) => ({durationInFrames: (props as unknown as ReelProps).totalFrames})}
  />
);
