import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { RootState } from '../modules';
import { getDashBardProfileAsync } from '../modules/dashboard';
import ReactExport from "react-export-excel";
import moment from 'moment';

import { Button, Table, Layout, Row, Col, Tabs, DatePicker, Input } from 'antd';
import 'antd/dist/antd.css';

function Dash_board() {

  const { Content } = Layout;
  const { TabPane } = Tabs;

  const dateFormat = 'YYYY-MM-DD';

  const ExcelFile = ReactExport.ExcelFile;
  const ExcelSheet = ReactExport.ExcelFile.ExcelSheet;
  //const ExcelColumn = ReactExport.ExcelFile.ExcelColumn;

  const { data, loading, error } = useSelector((state: RootState) => state.dashboard.dashboardProfile);
  const dispatch = useDispatch();

  const [tdata, setTdata] = useState([]);
  const [tdata3, setTdata3] = useState([]);
  const [originalData, setOriginalData] = useState([]);

  const [tkey, setTkey] = useState([]);

  const [filterData, setFilterData] = useState([]); 
  const [multiDataSet2, setMultiDataSet2] = useState([]);
  

  const test = (user:string) => {
    console.log("#user :" + user)
    dispatch(getDashBardProfileAsync.request(user));
   
       
  }


  const search = (searchInput:string) => {    
    console.log("PASS", { searchInput });

    /*const filterTable = tdata.filter(o =>
      Object.keys(o).some(k =>
        String(o[k])
          .toLowerCase()
          .includes(searchInput.toLowerCase())
      )
    );*/

    let filteredData = originalData.filter(value => {
      return (
        value.id.toLowerCase().includes(searchInput.toLowerCase()) ||
        value.name.toLowerCase().includes(searchInput.toLowerCase()) ||
        value.etc
          .toString()
          .toLowerCase()
          .includes(searchInput.toLowerCase())
      );
    });

    console.log("filterTable:", filteredData);

    setTdata(filteredData);
    //setState({ data: filteredData });
    
  };

  const columns = [
    {
      title: 'seq',
      dataIndex: 'seq',
      
      
    },
    {
      title: 'id',
      dataIndex: 'id',  
      
      
    },
    {
      title: 'name',
      dataIndex: 'name', 
      
      
    },
    {
      title: 'etc',
      dataIndex: 'etc',  
      
        
    },    
  ];

  
   
  const multiDataSet = [
    {
      columns: ["seq", "id", "name", "etc"],
      data: []
    },
  ];

  const check = () => {
    console.log("NO DATA~~~!!!")   
    
    return;
  }

  useEffect(() => {
        console.log('=== useEffect ===');

        
        if(data !== null){
          const j = Object.values(data);
        
          let tdata2 = [];
          let tkey2 = [];
          let test = [
            {
              columns: ["seq", "id", "name", "etc"],
              data: []
            }
          ];
          j && j.map((journal, index) => {          
            if(journal !== null){           
              let data1 = [{value: journal.seq.toString()},{value: journal.id},{value: journal.name},{value: journal.etc}];                 
              multiDataSet[0].data.push(data1)
              test[0].data.push(data1)              
              tdata2.push({seq: journal.seq, id: journal.id, name: journal.name, etc: journal.etc});
              tkey2.push(index);
              return  ( console.log("#t2 :" + journal.seq + journal.id + journal.name + journal.etc) )              
            } else {
              return  ( console.log("#t3 :" + journal ) )
            }          
            
            
          })

          setMultiDataSet2(test);

          setTdata(tdata2);
          setTdata([]);
          setTdata3(tdata2);
          setOriginalData(tdata2);
          setTkey(tkey2);
        }

        console.log("multiDataSet:", multiDataSet)

        console.log("data:",data)
        console.log("#tdata:",tdata)
        
             
        
        console.log("#loading :" + loading);
        console.log("#error :" + error);
  },[data, loading, error]);


  

  console.log("#tdata2:",tdata)
  return (
    <div>
      <Layout>      
        <Content>
          <Row>
            <Button type="primary" onClick={() => test("TEST") } >
              TEST
            </Button>
            {
                data === null ? <Button onClick={() => check() }>Excel</Button> :  
                <ExcelFile element={<Button>Excel</Button>} filename="TEST">
                  <ExcelSheet dataSet={multiDataSet2} name="Sheet1"/>
                </ExcelFile>       
            }
          </Row>          
          <Row>
            <DatePicker defaultValue={moment(new Date(), dateFormat)} format={dateFormat} />
          </Row>
          <Row>
              <Input.Search
              style={{ border: "3px solid red", margin: "0 0 10px 0" }}
              placeholder="Search by..."
              enterButton
              onSearch={search}
            />
          </Row>  
          <Row>
            <Tabs type="card">
              <TabPane tab="Tab 1" key="1">
                <Table columns={columns} dataSource={tdata} rowKey="seq" />  
              </TabPane>
              <TabPane tab="Tab 2" key="2">
              <Table columns={columns} dataSource={tdata3} rowKey="seq" />
              </TabPane>
              <TabPane tab="Tab 3" key="3">
                Content of Tab Pane 3
              </TabPane>
            </Tabs>
            
          </Row>
        </Content>      
      </Layout>
         
    </div>
  );
}


export default Dash_board;

//export default Dash_board;