import os
import os.path
import pycifstar

def test_answer():
    f_name = os.path.join(os.path.dirname(__file__), "example_1.cif")
    global_ = pycifstar.read_star_file(f_name)
    global_ = pycifstar.read_file(f_name)
    item = global_["_cell_length_a"]
    assert item.name == "_cell_length_a"
    assert item.value == "8.56212()"
    assert item.comment == "# object Cell - Fitable"
    
    item = global_["Fe3O4_cell_length_a"]
    assert item.name == "_cell_length_a"
    assert item.value == "8.56212()"
    assert item.comment == "# object Cell - Fitable"

    items = global_["_cell_length"]
    assert len(items) == 3
    assert items.names == ("_cell_length_a", "_cell_length_b", "_cell_length_c")

    loop = global_["_atom_site"]
    assert loop.names == ("_atom_site_adp_type", "_atom_site_b_iso_or_equiv", 
        "_atom_site_fract_x", "_atom_site_fract_y", "_atom_site_fract_z", 
        "_atom_site_label", "_atom_site_occupancy", "_atom_site_type_symbol")
    
    data = global_["Fe3O4"]
    assert data.name == "Fe3O4"

    item = pycifstar.Item(name="_jh", value="sf", comment="jhklj")
    loop = pycifstar.Loop(names=("_jh_2", "_jh_zzz"), values=(("1", "2"), ("11", "22"), ("111", "222")))

    data_block = pycifstar.Data()
    data_block.add_item(item)
    data_block.add_loop(loop)

    global_["_cell_length_a"].value = 8.3
    global_["_cell_length_a"].comment = "comment line"
    print(global_)
    
def test_answer_2():
    f_name = os.path.join(os.path.dirname(__file__), "example_2.cif")
    global_ = pycifstar.read_star_file(f_name)
    global_ = pycifstar.read_file(f_name)
    items = global_["_cell"]

    assert len(items) == 6
    assert items.names == ("_cell.angle_alpha", "_cell.angle_beta", "_cell.angle_gamma",
                           "_cell.length_a", "_cell.length_b", "_cell.length_c")
    assert items["_cell.angle_alpha"].value == "90.0"

    loop = global_["_atom_site"]
    assert loop.names == ("_atom_site.adp_type", "_atom_site.b_iso_or_equiv", 
        "_atom_site.fract_x", "_atom_site.fract_y", "_atom_site.fract_z", 
        "_atom_site.label", "_atom_site.occupancy", "_atom_site.type_symbol")
    assert loop["_atom_site.adp_type"] == ["uani", "uani", "uiso"]
    




