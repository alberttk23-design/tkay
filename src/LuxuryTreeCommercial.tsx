import React from "react";
import {
  AbsoluteFill,
  Audio,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Video,
} from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

/**
 * Luxury Christmas Tree Commercial - 60FPS Butter-Smooth (NO JITTER, NO TEXT)
 * 5 Smooth 60fps Scenes with Deflicker, Cinematic Warm Transitions, Luxury BGM
 */
export const LuxuryTreeCommercial: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // BGM volume automation: subtle fade-in and smooth fade-out at the end
  const bgmVolume = interpolate(
    frame,
    [0, 30, durationInFrames - 60, durationInFrames],
    [0, 0.9, 0.9, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );

  const TRANSITION_DURATION = 28; // 28 frames at 60fps (~0.46s) smooth dissolve

  return (
    <AbsoluteFill style={{ backgroundColor: "#000000" }}>
      {/* 5-Scene 60FPS Cinematic Transition Sequence */}
      <TransitionSeries>
        {/* Scene 1: Ambiance Hook - Warm holiday lighting ignites the room */}
        <TransitionSeries.Sequence durationInFrames={220}>
          <Video
            src={staticFile("assets/smooth_tree_tvc/scene1_ambiance.mp4")}
            startFrom={30}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_DURATION })}
        />

        {/* Scene 2: Camera glide toward the majestic Christmas tree */}
        <TransitionSeries.Sequence durationInFrames={190}>
          <Video
            src={staticFile("assets/smooth_tree_tvc/scene2_glide.mp4")}
            startFrom={20}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_DURATION })}
        />

        {/* Scene 3: Macro Texture - Hand gently touching realistic evergreen foliage */}
        <TransitionSeries.Sequence durationInFrames={190}>
          <Video
            src={staticFile("assets/smooth_tree_tvc/scene3_needles.mp4")}
            startFrom={30}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_DURATION })}
        />

        {/* Scene 4: Sparkling Details - Ornament & warm fairy light twinkle */}
        <TransitionSeries.Sequence durationInFrames={190}>
          <Video
            src={staticFile("assets/smooth_tree_tvc/scene4_ornament.mp4")}
            startFrom={30}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_DURATION })}
        />

        {/* Scene 5: Grand Hero Reveal - Full Christmas tree standing proud */}
        <TransitionSeries.Sequence durationInFrames={240}>
          <Video
            src={staticFile("assets/smooth_tree_tvc/scene5_reveal.mp4")}
            startFrom={20}
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        </TransitionSeries.Sequence>
      </TransitionSeries>

      {/* Subtle Cinematic Warm Vignette (Enhances luxury tree glow without any text) */}
      <AbsoluteFill
        style={{
          background:
            "radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.4) 100%)",
          pointerEvents: "none",
        }}
      />

      {/* Luxury Holiday BGM Track */}
      <Audio
        src={staticFile("assets/audio/bgm_christmas_luxury.mp3")}
        volume={bgmVolume}
      />
    </AbsoluteFill>
  );
};
