import React from "react";
import {
  AbsoluteFill,
  Audio,
  interpolate,
  Sequence,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  Video,
} from "remotion";

interface SceneProps {
  videoSrc: string;
  startFromFrame: number;
  badge?: string;
  title: string;
  subtitle: string;
  durationFrames: number;
}

const CleanSceneSlide: React.FC<SceneProps> = ({
  videoSrc,
  startFromFrame,
  badge,
  title,
  subtitle,
  durationFrames,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Subtle clean fade for first 4 frames
  const opacity = interpolate(frame, [0, 4], [0.3, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Text Spring Animation
  const titleSpring = spring({
    frame: frame - 4,
    fps,
    config: { damping: 15, stiffness: 90 },
  });
  const translateY = interpolate(titleSpring, [0, 1], [30, 0]);

  return (
    <AbsoluteFill style={{ opacity }}>
      {/* Native Raw Video - 100% Crisp & Smooth */}
      <AbsoluteFill>
        <Video
          src={staticFile(videoSrc)}
          startFrom={startFromFrame}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
        />
      </AbsoluteFill>

      {/* Subtle Bottom Gradient for Typography */}
      <AbsoluteFill
        style={{
          background:
            "linear-gradient(to top, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.2) 25%, rgba(0,0,0,0) 50%)",
        }}
      />

      {/* Typography Overlay */}
      <div
        style={{
          position: "absolute",
          bottom: 160,
          left: 60,
          right: 60,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          textAlign: "center",
          transform: `translateY(${translateY}px)`,
          opacity: Math.max(0, titleSpring),
        }}
      >
        {badge && (
          <div
            style={{
              padding: "8px 22px",
              borderRadius: 30,
              backgroundColor: "rgba(185, 28, 28, 0.95)",
              color: "#ffffff",
              fontSize: 20,
              fontWeight: 800,
              letterSpacing: 2,
              textTransform: "uppercase",
              marginBottom: 12,
              boxShadow: "0 4px 16px rgba(0,0,0,0.5)",
              border: "1px solid rgba(255,255,255,0.3)",
            }}
          >
            {badge}
          </div>
        )}

        <h1
          style={{
            color: "#ffffff",
            fontSize: 54,
            fontWeight: 900,
            lineHeight: 1.15,
            margin: 0,
            textShadow: "0 4px 20px rgba(0,0,0,0.9)",
            letterSpacing: "-0.5px",
            fontFamily: "system-ui, -apple-system, sans-serif",
          }}
        >
          {title}
        </h1>

        <p
          style={{
            color: "#fde047",
            fontSize: 28,
            fontWeight: 700,
            marginTop: 10,
            marginBottom: 0,
            textShadow: "0 2px 12px rgba(0,0,0,0.9)",
            fontFamily: "system-ui, -apple-system, sans-serif",
          }}
        >
          {subtitle}
        </p>
      </div>
    </AbsoluteFill>
  );
};

export const FamilyChristmasTVC: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#000000" }}>
      {/* Emotional Holiday Voiceover */}
      <Audio src={staticFile("assets/family_voiceover.mp3")} />

      {/* Scene 1 (0 - 72 frames ~ 3.0s): Bé che mắt rồi mở mắt ngạc nhiên cực nét, không bị giật */}
      <Sequence from={0} durationInFrames={72}>
        <CleanSceneSlide
          videoSrc="assets/family_clean/clip1_lead.mp4"
          startFromFrame={60} // start from 2.5s where she opens her eyes smoothly
          badge="THE MAGIC BEGINS"
          title="Close Your Eyes..."
          subtitle="And Make A Wish"
          durationFrames={72}
        />
      </Sequence>

      {/* Scene 2 (72 - 168 frames ~ 4.0s): Camera lia mượt mà hé lộ full cây thông */}
      <Sequence from={72} durationInFrames={96}>
        <CleanSceneSlide
          videoSrc="assets/family_clean/clip2_reveal.mp4"
          startFromFrame={48} // 2.0s
          badge="THE REVEAL"
          title="Pure Holiday Wonder"
          subtitle="Brought To Life"
          durationFrames={96}
        />
      </Sequence>

      {/* Scene 3 (168 - 252 frames ~ 3.5s): Bé đứng ngắm nhìn mê mẩn cây thông */}
      <Sequence from={168} durationInFrames={84}>
        <CleanSceneSlide
          videoSrc="assets/family_clean/clip3_admire.mp4"
          startFromFrame={24} // 1.0s
          badge="TIMELESS BEAUTY"
          title="Shining Bright"
          subtitle="In Every Detail"
          durationFrames={84}
        />
      </Sequence>

      {/* Scene 4 (252 - 396 frames ~ 6.0s): Bố mẹ gọi, bé chạy lại, cả nhà hạnh phúc bên cây thông */}
      <Sequence from={252} durationInFrames={144}>
        <CleanSceneSlide
          videoSrc="assets/family_clean/clip5_hug.mp4"
          startFromFrame={0} // Smooth opening from 0s where parents call and girl hugs
          badge="FAMILY TRADITIONS"
          title="The Heart Of Home"
          subtitle="Bring The Magic Home"
          durationFrames={144}
        />
      </Sequence>
    </AbsoluteFill>
  );
};
