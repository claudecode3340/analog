/** Registry for FigureSpec (problems and lesson steps): a key → a parametric figure. */
import {
  ChannelCrossSection,
  CsSmallSignal,
  IdVdsFamily,
  MosBias,
  NmosRd,
  ParallelPair,
  PmosRd,
  ResStack,
  SmallSignalModel,
  TransferCurve,
  WaterAnalogy,
} from './figures';
import { CascodeFig, CommonGateFig, CsLoadFig, FollowerFig, ImpedanceFig, MirrorFig, TelescopicFig } from './figures2';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const FIGURES: Record<string, (props: any) => React.ReactElement> = {
  water: WaterAnalogy,
  resStack: ResStack,
  parallelPair: ParallelPair,
  mosBias: MosBias,
  channel: ChannelCrossSection,
  idvds: IdVdsFamily,
  nmosRd: NmosRd,
  pmosRd: PmosRd,
  smallSignalModel: SmallSignalModel,
  csSmallSignal: CsSmallSignal,
  transfer: TransferCurve,
  impedance: ImpedanceFig,
  mirror: MirrorFig,
  csLoad: CsLoadFig,
  follower: FollowerFig,
  commonGate: CommonGateFig,
  cascode: CascodeFig,
  telescopic: TelescopicFig,
};

export function Figure({ kind, props, highlight }: { kind: string; props?: Record<string, unknown>; highlight?: string[] }) {
  const C = FIGURES[kind];
  if (!C) return <p className="callout bad">Missing figure: {kind}</p>;
  return <C {...(props ?? {})} highlight={highlight} />;
}
