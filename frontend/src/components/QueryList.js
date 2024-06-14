import React, { Component } from "react";
import { Table } from "reactstrap";
import NewQueryModal from "./NewQueryModal";
import ConfirmRemovalModal from "./ConfirmRemovalModal";

class QueryList extends Component {
  render() {
    const queries = this.props.queries;
    return (
      <Table dark>
        <thead>
          <tr>
            <th>Model</th>
            <th>Model Version</th>
            <th>Query Input</th>
            <th>Query Output</th>
            <th>Created At</th>
            <th>Updated At</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {!queries || queries.length <= 0 ? (
            <tr>
              <td colSpan="7" align="center">
                <b>Ops, no queries here yet</b>
              </td>
            </tr>
          ) : (
            queries.map(query => (
              <tr key={query.pk}>
                <td>{query.model}</td>
                <td>{query.modelv}</td>
                <td>{JSON.stringify(query.query_input)}</td>
                <td>{JSON.stringify(query.query_output)}</td>
                <td>{query.created_at}</td>
                <td>{query.updated_at}</td>
                <td align="center">
                  <NewQueryModal
                    create={false}
                    query={query}
                    resetState={this.props.resetState}
                  />
                  &nbsp;&nbsp;
                  <ConfirmRemovalModal
                    pk={query.pk}
                    resetState={this.props.resetState}
                  />
                </td>
              </tr>
            ))
          )}
        </tbody>
      </Table>
    );
  }
}

export default QueryList;
