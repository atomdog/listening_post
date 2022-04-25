import React, { FC, useEffect, useMemo, useState } from "react";
import { useSigma } from "react-sigma-v2";
import { MdCategory } from "react-icons/md";
import { keyBy, mapValues, sortBy, values } from "lodash";
import { AiOutlineCheckCircle, AiOutlineCloseCircle } from "react-icons/ai";

import { FiltersState, Source } from "../types";
import Panel from "./Panel";

const SourcesPanel: FC<{
  sources: Source[];
  filters: FiltersState;
  toggleSource: (source: string) => void;
  setSources: (Sources: Record<string, boolean>) => void;
}> = ({ sources, filters, toggleSource, setSources }) => {
  const sigma = useSigma();
  const graph = sigma.getGraph();

  const nodesPerSource = useMemo(() => {
    const index: Record<string, number> = {};
    graph.forEachNode((_, { source }) => (index[source] = (index[source] || 0) + 1));
    return index;
  }, []);

  const maxNodesPerSource = useMemo(() => Math.max(...values(nodesPerSource)), [nodesPerSource]);
  const visibleSourceCount = useMemo(() => Object.keys(filters.sources).length, [filters]);

  const [visibleNodesPerSource, setVisibleNodesPerSource] = useState<Record<string, number>>(nodesPerSource);
  useEffect(() => {
    // To ensure the graphology instance has up to data "hidden" values for
    // nodes, we wait for next frame before reindexing. This won't matter in the
    // UX, because of the visible nodes bar width transition.
    requestAnimationFrame(() => {
      const index: Record<string, number> = {};
      graph.forEachNode((_, { source, hidden }) => !hidden && (index[source] = (index[source] || 0) + 1));
      setVisibleNodesPerSource(index);
    });
  }, [filters]);

  const sortedSources = useMemo(
    () => sortBy(sources, (source) => (source.key === "unknown" ? Infinity : -nodesPerSource[source.key])),
    [sources, nodesPerSource],
  );

  return (
    <Panel
      title={
        <>
          <MdCategory className="text-muted" /> Sources
          {visibleSourceCount < sources.length ? (
            <span className="text-muted text-small">
              {" "}
              ({visibleSourceCount} / {sources.length})
            </span>
          ) : (
            ""
          )}
        </>
      }
    >
      <p>
        <i className="text-muted">Click a category to show/hide related pages from the network.</i>
      </p>
      <p className="buttons">
        <button className="btn" onClick={() => setSources(mapValues(keyBy(sources, "key"), () => true))}>
          <AiOutlineCheckCircle /> Check all
        </button>{" "}
        <button className="btn" onClick={() => setSources({})}>
          <AiOutlineCloseCircle /> Uncheck all
        </button>
      </p>
      <ul>
        {sortedSources.map((source) => {
          const nodesCount = nodesPerSource[source.key];
          const visibleNodesCount = visibleNodesPerSource[source.key] || 0;
          return (
            <li
              className="caption-row"
              key={source.key}
              title={`${nodesCount} page${nodesCount > 1 ? "s" : ""}${
                visibleNodesCount !== nodesCount ? ` (only ${visibleNodesCount} visible)` : ""
              }`}
            >
              <input
                type="checkbox"
                checked={filters.sources[source.key] || false}
                onChange={() => toggleSource(source.key)}
                id={`source-${source.key}`}
              />
              <label htmlFor={`source-${source.key}`}>
                <span
                  className="circle"
                  style={{ backgroundImage: `url(${process.env.PUBLIC_URL}/images/${source.image})` }}
                />{" "}
                <div className="node-label">
                  <span>{source.key}</span>
                  <div className="bar" style={{ width: (100 * nodesCount) / maxNodesPerSource + "%" }}>
                    <div
                      className="inside-bar"
                      style={{
                        width: (100 * visibleNodesCount) / nodesCount + "%",
                      }}
                    />
                  </div>
                </div>
              </label>
            </li>
          );
        })}
      </ul>
    </Panel>
  );
};

export default SourcesPanel;
