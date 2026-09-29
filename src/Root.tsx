import "./index.css";
import { Composition } from "remotion";
import { FamilyChristmasTVC } from "./FamilyChristmasTVC";
import { LuxuryTreeCommercial } from "./LuxuryTreeCommercial";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="LuxuryTreeCommercial"
        component={LuxuryTreeCommercial}
        durationInFrames={918}
        fps={60}
        width={1080}
        height={1920}
      />
      <Composition
        id="FamilyChristmasTVC"
        component={FamilyChristmasTVC}
        durationInFrames={396}
        fps={24}
        width={1080}
        height={1920}
      />
    </>
  );
};
