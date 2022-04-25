export interface NodeData {
  key: string;
  label: string;
  tag: string;
  date_spoken: string;
  source: string;
  url: string;
  score: number;
  cluster: string;
  x: number;
  y: number;
}

export interface Cluster {
  key: string;
  color: string;
  clusterLabel: string;
}

export interface Tag {
  key: string;
  image: string;
}

export interface Source {
  key: string;
  image: string;
}

export interface Dataset {
  nodes: NodeData[];
  edges: [string, string][];
  clusters: Cluster[];
  sources: Source[];
  tags: Tag[];

}

export interface FiltersState {
  clusters: Record<string, boolean>;
  tags: Record<string, boolean>;
  sources: Record<string, boolean>;
}
