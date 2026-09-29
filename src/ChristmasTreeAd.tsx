import React from "react";
import {
  AbsoluteFill,
  Audio,
  Img,
  interpolate,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Video,
} from "remotion";

// Snowflake component for cinematic snowfall effect
const SnowOverlay: React.FC = () => {
  const frame = useCurrentFrame();
  const flakes = React.useMemo(() => {
    return Array.from({ length: 35 }).map((_, i) => ({
      id: i,
      x: (i * 31) % 100,
      size: 4 + ((i * 7) % 8),
      speed: 1.2 + ((i * 3) % 2.5),
      opacity: 0.35 + ((i * 5) % 0.55),
      delay: (i * 13) % 100,
    }));
  }, []);

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {flakes.map((f) => {
        const y = ((frame * f.speed + f.delay * 10) % 2000) - 80;
        const drift = Math.sin((frame + f.delay) * 0.03) * 20;
        return (
          <div
            key={f.id}
            style={{
              position: "absolute",
              left: `${f.x}%`,
              top: `${y}px`,
              transform: `translateX(${drift}px)`,
              width: f.size,
              height: f.size,
              borderRadius: "50%",
              backgroundColor: "white",
              opacity: f.opacity,
              boxShadow: "0 0 10px rgba(255,255,255,0.9)",
            }}
          />
        );
      })}
    </AbsoluteFill>
  );
};

interface SceneProps {
  mediaSrc: string;
  isVideo?: boolean;
  badge?: string;
  title: string;
  subtitle: string;
  startFrame: number;
  durationFrames: number;
  zoomDirection?: "in" | "out";
}

const SceneSlide: React.FC<SceneProps> = ({
  mediaSrc,
  isVideo = false,
  badge,
  title,
  subtitle,
  startFrame,
  durationFrames,
  zoomDirection = "in",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const localFrame = frame - startFrame;
  if (localFrame < 0 || localFrame >= durationFrames) {
    return null;
  }

  // Crossfade opacity
  const fadeIn = interpolate(localFrame, [0, 12], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const fadeOut = interpolate(
    localFrame,
    [durationFrames - 12, durationFrames],
    [1, 0],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    }
  );
  const opacity = Math.min(fadeIn, fadeOut);

  // Ken Burns zoom effect
  const scale =
    zoomDirection === "in"
      ? interpolate(localFrame, [0, durationFrames], [1.0, 1.08], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        })
      : interpolate(localFrame, [0, durationFrames], [1.08, 1.01], {
          extrapolateLeft: "clamp",
          extrapolateRight: "clamp",
        });

  // Text Spring Animation
  const titleSpring = spring({
    frame: localFrame - 5,
    fps,
    config: { damping: 14, stiffness: 90 },
  });

  const titleTranslateY = interpolate(titleSpring, [0, 1], [40, 0]);

  return (
    <AbsoluteFill style={{ opacity }}>
      {/* Background Media (Real Video or High-res Image) */}
      <AbsoluteFill
        style={{
          transform: `scale(${scale})`,
          transformOrigin: "center center",
        }}
      >
        {isVideo ? (
          <Video
            src={staticFile(mediaSrc)}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
          />
        ) : (
          <Img
            src={staticFile(mediaSrc)}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
          />
        )}
      </AbsoluteFill>

      {/* Cinematic Vignette & Bottom Gradient */}
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.25) 30%, rgba(0,0,0,0) 60%, rgba(0,0,0,0.4) 100%)",
        }}
      />

      {/* Typography Overlay */}
      <div
        style={{
          position: "absolute",
          bottom: 180,
          left: 60,
          right: 60,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          textAlign: "center",
          transform: `translateY(${titleTranslateY}px)`,
          opacity: Math.max(0, titleSpring),
        }}
      >
        {badge && (
          <div
            style={{
              padding: "10px 24px",
              borderRadius: 30,
              backgroundColor: "rgba(220, 38, 38, 0.95)",
              color: "#ffffff",
              fontSize: 22,
              fontWeight: 800,
              letterSpacing: 2.5,
              textTransform: "uppercase",
              marginBottom: 16,
              boxShadow: "0 4px 20px rgba(220,38,38,0.6)",
              border: "1px solid rgba(255,255,255,0.4)",
            }}
          >
            {badge}
          </div>
        )}

        <h1
          style={{
            color: "#ffffff",
            fontSize: 58,
            fontWeight: 900,
            lineHeight: 1.1,
            margin: 0,
            textShadow: "0 4px 24px rgba(0,0,0,0.9)",
            letterSpacing: "-1px",
            fontFamily: "system-ui, -apple-system, sans-serif",
          }}
        >
          {title}
        </h1>

        <p
          style={{
            color: "#fde047",
            fontSize: 32,
            fontWeight: 700,
            marginTop: 12,
            marginBottom: 0,
            textShadow: "0 2px 14px rgba(0,0,0,0.9)",
            fontFamily: "system-ui, -apple-system, sans-serif",
          }}
        >
          {subtitle}
        </p>
      </div>
    </AbsoluteFill>
  );
};

export const ChristmasTreeAd: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#000000" }}>
      {/* English Commercial Voiceover */}
      <Audio src={staticFile("assets/voiceover_en.mp3")} />

      {/* Scene 1 (0 - 95 frames ~ 3.1s): REAL MOTION VIDEO - Woman clicking remote */}
      <SceneSlide
        mediaSrc="assets/real_motion_scene1.mp4"
        isVideo={true}
        badge="SMART MAGIC"
        title="JUST ONE CLICK"
        subtitle="The Holiday Season Comes Alive"
        startFrame={0}
        durationFrames={95}
        zoomDirection="in"
      />

      {/* Scene 2 (85 - 175 frames ~ 3.0s): REAL MOTION VIDEO - Woman snapping fingers */}
      <SceneSlide
        mediaSrc="assets/real_motion_scene2.mp4"
        isVideo={true}
        badge="EASY SETUP"
        title="SNAP & DONE!"
        subtitle="Zero Effort. Pure Magic."
        startFrame={85}
        durationFrames={95}
        zoomDirection="out"
      />

      {/* Scene 3 (170 - 260 frames ~ 3.0s): REAL MOTION VIDEO - Roaring fireplace & snowfall */}
      <SceneSlide
        mediaSrc="assets/real_motion_scene3.mp4"
        isVideo={true}
        badge="COZY CABIN"
        title="WARM & RUSTIC"
        subtitle="Nordic Alpine Comfort"
        startFrame={170}
        durationFrames={95}
        zoomDirection="in"
      />

      {/* Scene 4 (255 - 345 frames ~ 3.0s): Minimalist Japandi */}
      <SceneSlide
        mediaSrc="assets/scene4_minimal.jpg"
        isVideo={false}
        badge="WARM MINIMALIST"
        title="CLEAN & SERENE"
        subtitle="Effortless Elegance Anywhere"
        startFrame={255}
        durationFrames={95}
        zoomDirection="out"
      />

      {/* Scene 5 (340 - 450 frames ~ 3.6s): Luxury Penthouse & Climax */}
      <SceneSlide
        mediaSrc="assets/scene5_penthouse.jpg"
        isVideo={false}
        badge="LUXURY LIVING"
        title="PERFECTION"
        subtitle="In Every Single Space"
        startFrame={340}
        durationFrames={110}
        zoomDirection="in"
      />

      {/* Snow Particles overlay on top of all scenes */}
      <SnowOverlay />
    </AbsoluteFill>
  );
};
