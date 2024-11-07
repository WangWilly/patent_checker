import React, { useState } from 'react';
import { Text, View, TextInput, Button, ActivityIndicator, ScrollView, FlatList } from 'react-native';
import { fetcher } from '../core/fetcher';
import { PatentInfringement, Product, AssessInfringementV1 } from '../core/dtos';

export default function Searcher() {
  const [infringement_id, setInfringementId] = useState('');
  const [result, setResult] = useState(null as null | PatentInfringement);
  const [loading, setLoading] = useState(false);
  const [notFound, setNotFound] = useState(false);

  const fetchData = () => {
    setLoading(true);

    setResult(null);
    setNotFound(false);
    fetcher
      .get<any>(
        `/infringement/v1/${infringement_id}`,
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

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', padding: 20 }}>
      <TextInput
        placeholder="Infringement ID"
        value={infringement_id}
        onChangeText={setInfringementId}
        style={{ height: 40, borderColor: 'gray', borderWidth: 1, marginBottom: 10, width: '80%', paddingHorizontal: 10 }}
      />
      <Button onPress={fetchData} title="Search"/>
      {loading && <Text>Loading...</Text>}
      {result && (
          <ScrollView>
          <Text style={{ fontWeight: 'bold', fontSize: 16 }}>Patent ID: {result.patent_id}</Text>
          <Text>Company Name: {result.company_name}</Text>
          <Text>Analysis Date: {result.analysis_date}</Text>
          <Text style={{ fontWeight: 'bold', marginTop: 10 }}>Overall Risk Assessment:</Text>
          <Text>{result.overall_risk_assessment}</Text>
          {/* <Text>Top infringing products: {result.top_infringing_products}</Text> */}
          </ScrollView>
      )}
      {notFound && <Text style={{ color: 'red' }}>Checking record not found</Text>}
    </View>
    );
}
