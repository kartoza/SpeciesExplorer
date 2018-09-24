<!DOCTYPE qgis PUBLIC 'http://mrcc.com/qgis.dtd' 'SYSTEM'>
<qgis version="3.3.0-Master">
  <renderer-v2 toleranceUnit="MM" toleranceUnitScale="3x:0,0,0,0,0,0" tolerance="14" type="pointCluster" enableorderby="0" forceraster="0">
    <renderer-v2 symbollevels="0" type="singleSymbol" enableorderby="0" forceraster="0">
      <symbols>
        <symbol clip_to_extent="1" alpha="1" type="marker" name="0">
          <layer locked="0" enabled="1" pass="0" class="SimpleMarker">
            <prop k="angle" v="0"/>
            <prop k="color" v="243,166,178,255"/>
            <prop k="horizontal_anchor_point" v="1"/>
            <prop k="joinstyle" v="bevel"/>
            <prop k="name" v="circle"/>
            <prop k="offset" v="0,0"/>
            <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="offset_unit" v="MM"/>
            <prop k="outline_color" v="35,35,35,255"/>
            <prop k="outline_style" v="solid"/>
            <prop k="outline_width" v="0"/>
            <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="outline_width_unit" v="MM"/>
            <prop k="scale_method" v="diameter"/>
            <prop k="size" v="4"/>
            <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
            <prop k="size_unit" v="MM"/>
            <prop k="vertical_anchor_point" v="1"/>
            <data_defined_properties>
              <Option type="Map">
                <Option type="QString" value="" name="name"/>
                <Option name="properties"/>
                <Option type="QString" value="collection" name="type"/>
              </Option>
            </data_defined_properties>
          </layer>
        </symbol>
      </symbols>
      <rotation/>
      <sizescale/>
    </renderer-v2>
    <symbol clip_to_extent="1" alpha="1" type="marker" name="centerSymbol">
      <layer locked="0" enabled="1" pass="0" class="SimpleMarker">
        <prop k="angle" v="0"/>
        <prop k="color" v="245,75,80,255"/>
        <prop k="horizontal_anchor_point" v="1"/>
        <prop k="joinstyle" v="bevel"/>
        <prop k="name" v="circle"/>
        <prop k="offset" v="0,0"/>
        <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
        <prop k="offset_unit" v="MM"/>
        <prop k="outline_color" v="35,35,35,255"/>
        <prop k="outline_style" v="solid"/>
        <prop k="outline_width" v="0"/>
        <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
        <prop k="outline_width_unit" v="MM"/>
        <prop k="scale_method" v="diameter"/>
        <prop k="size" v="12"/>
        <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
        <prop k="size_unit" v="MM"/>
        <prop k="vertical_anchor_point" v="1"/>
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" value="" name="name"/>
            <Option type="Map" name="properties">
              <Option type="Map" name="size">
                <Option type="bool" value="false" name="active"/>
                <Option type="QString" value="" name="expression"/>
                <Option type="int" value="3" name="type"/>
              </Option>
            </Option>
            <Option type="QString" value="collection" name="type"/>
          </Option>
        </data_defined_properties>
      </layer>
      <layer locked="0" enabled="1" pass="0" class="FontMarker">
        <prop k="angle" v="0"/>
        <prop k="chr" v="A"/>
        <prop k="color" v="36,32,35,255"/>
        <prop k="font" v="Arial"/>
        <prop k="horizontal_anchor_point" v="1"/>
        <prop k="joinstyle" v="miter"/>
        <prop k="offset" v="0,-1"/>
        <prop k="offset_map_unit_scale" v="3x:0,0,0,0,0,0"/>
        <prop k="offset_unit" v="MM"/>
        <prop k="outline_color" v="36,32,35,255"/>
        <prop k="outline_width" v="0"/>
        <prop k="outline_width_map_unit_scale" v="3x:0,0,0,0,0,0"/>
        <prop k="outline_width_unit" v="MM"/>
        <prop k="size" v="5"/>
        <prop k="size_map_unit_scale" v="3x:0,0,0,0,0,0"/>
        <prop k="size_unit" v="MM"/>
        <prop k="vertical_anchor_point" v="1"/>
        <data_defined_properties>
          <Option type="Map">
            <Option type="QString" value="" name="name"/>
            <Option type="Map" name="properties">
              <Option type="Map" name="char">
                <Option type="bool" value="true" name="active"/>
                <Option type="QString" value="@cluster_size" name="expression"/>
                <Option type="int" value="3" name="type"/>
              </Option>
              <Option type="Map" name="offset">
                <Option type="bool" value="true" name="active"/>
                <Option type="QString" value="'0'|| ',' || tostring(-0.1*())" name="expression"/>
                <Option type="int" value="3" name="type"/>
              </Option>
              <Option type="Map" name="size">
                <Option type="bool" value="false" name="active"/>
                <Option type="int" value="1" name="type"/>
                <Option type="QString" value="" name="val"/>
              </Option>
            </Option>
            <Option type="QString" value="collection" name="type"/>
          </Option>
        </data_defined_properties>
      </layer>
    </symbol>
  </renderer-v2>
  <blendMode>0</blendMode>
  <featureBlendMode>0</featureBlendMode>
  <layerGeometryType>0</layerGeometryType>
</qgis>
