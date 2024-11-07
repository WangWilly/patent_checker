import React, { useState } from 'react';
import { Text, View, TextInput, Button, ActivityIndicator, ScrollView, FlatList } from 'react-native';
import { fetcher } from '../core/fetcher';
import { PatentInfringement, Product, AssessInfringementV1 } from '../core/dtos';

////////////////////////////////////////////////////////////////////////////////

export default function Index() {
  const [patentPubId, setPatentPubId] = useState('');
  const [companyName, setCompanyName] = useState('');
  const [result, setResult] = useState(null as null | PatentInfringement);
  const [loading, setLoading] = useState(false);
  const [createResp, setCreateResp] = useState(null as null | AssessInfringementV1);
  const [uploading, setUploading] = useState(false);
  const [notFound, setNotFound] = useState(false);

  const fetchData = () => {
    setLoading(true);

    setResult(null);
    setCreateResp(null);
    setNotFound(false);
    fetcher
      .post<any>(
        '/gpt/v1/assess_infringement',
        { 'patent_pub_id': patentPubId, 'company_name': companyName },
      )
      .then((res) => {
        setResult(res.data);
      })
      .catch((err) => {
        console.error(err);
        setNotFound(true);
      })
      .finally(() => {
        setLoading(false);
      });
  }

  const renderProduct = ({ item }: { item: Product }) => (
    <View style={{ marginBottom: 10 }}>
      <Text style={{ fontWeight: 'bold' }}>{item.product_name}</Text>
      <Text>Infringement Likelihood: {item.infringement_likelihood}</Text>
      <Text>Relevant Claims: {item.relevant_claims.join(', ')}</Text>
      <Text>Explanation: {item.explanation}</Text>
      <Text>Specific Features: {item.specific_features.join(', ')}</Text>
    </View>
  );

  //////////////////////////////////////////////////////////////////////////////

  const uploadResult = async () => {
    try {
      setUploading(true);
      const response = await fetcher.post<any>('/infringement/v1', result);
      setCreateResp(response.data);
      setUploading(false);
    } catch (error) {
      console.error('Error uploading result:', error);
    }
  };
  
  const UploadButton = () => (
    <Button onPress={uploadResult} title="Upload Result"/>
  );

  //////////////////////////////////////////////////////////////////////////////

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 }}>
      <TextInput
        placeholder="Enter Patent Pub ID"
        value={patentPubId}
        onChangeText={setPatentPubId}
        style={{ height: 40, borderColor: 'gray', borderWidth: 1, marginBottom: 10, width: '80%', paddingHorizontal: 10 }}
      />
      <TextInput
        placeholder="Enter Company Name"
        value={companyName}
        onChangeText={setCompanyName}
        style={{ height: 40, borderColor: 'gray', borderWidth: 1, marginBottom: 10, width: '80%', paddingHorizontal: 10 }}
      />
      <Button title="Check infringement" onPress={fetchData} />

      {loading ? (
        <ActivityIndicator size="large" color="#0000ff" />
      ) : (
        result && (
          <ScrollView style={{ marginTop: 20, width: '100%' }}>
            <Text style={{ fontWeight: 'bold', fontSize: 16 }}>Patent ID: {result.patent_id}</Text>
            <Text>Company Name: {result.company_name}</Text>
            <Text>Analysis Date: {new Date(result.analysis_date).toLocaleDateString()}</Text>
            <Text style={{ fontWeight: 'bold', marginTop: 10 }}>Top Infringing Products:</Text>
            <FlatList
              data={result.top_infringing_products}
              renderItem={renderProduct}
              keyExtractor={(item, index) => index.toString()}
            />
            <Text style={{ fontWeight: 'bold', marginTop: 10 }}>Overall Risk Assessment:</Text>
            <Text>{result.overall_risk_assessment}</Text>
          </ScrollView>
        )
      )}

      {result && (
        <View style={{ height: 20, marginTop: 20 }}>
          {uploading ? (
              <ActivityIndicator size="large" color="#0000ff" />
          ) : (
            createResp ? (
              <Text style={{ fontWeight: 'bold', fontSize: 16 }}>🍭 Result uploaded successfully with ID: {createResp.id}</Text>
            ) : (
              <UploadButton />
            )
          )}
        </View>
      )}

      {notFound && <Text style={{ color: 'red' }}>There is no record in our database for the given Patent Pub ID or Company Name</Text>}
    </View>
  );
}
