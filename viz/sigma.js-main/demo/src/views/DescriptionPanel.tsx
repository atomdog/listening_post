import React, { FC } from "react";
import { BsInfoCircle } from "react-icons/bs";

import Panel from "./Panel";

const DescriptionPanel: FC = () => {
  return (
    <Panel
      initiallyDeployed
      title={
        <>
          <BsInfoCircle className="text-muted" /> Description
        </>
      }
    >


      <p>
        Nodes are displayed as they were spoken with minimal cleaning for legibility.
      </p>
    </Panel>
  );
};

export default DescriptionPanel;
